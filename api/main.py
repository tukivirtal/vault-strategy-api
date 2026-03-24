from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import json
from supabase import create_client, Client

app = FastAPI()

# ==========================================
# 1. CONFIGURACIÓN DE SEGURIDAD (CORS)
# El asterisco (*) permite que Vercel se conecte sin ser bloqueado
# ==========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# ==========================================
# 2. CONEXIÓN A LA BASE DE DATOS (SUPABASE)
# ==========================================
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ==========================================
# 3. MODELOS DE DATOS (Lo que envía Vercel)
# ==========================================
class LoginData(BaseModel):
    email: str
    password: str
    login_only: bool = False
    nombre: str = None
    lugar: str = None
    fecha: str = None
    hora: str = None
    lat: str = None
    lon: str = None

class PerfilRequest(BaseModel):
    email: str

# ==========================================
# 4. RUTAS DEL "CEREBRO" (API)
# ==========================================

@app.post("/consultar")
async def consultar(data: LoginData):
    """
    Ruta para procesar el Registro y el Login desde portal.html
    """
    if not supabase:
        return {"status": "error", "analisis_ejecutivo": "Error interno: Base de datos no conectada."}
        
    try:
        # Buscamos si el usuario ya existe en Supabase (asumimos que la tabla se llama 'usuarios')
        # NOTA: Si tu tabla se llama distinto (ej. 'users'), cambia "usuarios" por tu nombre real
        response = supabase.table("clientes_vip").select("*").eq("email", data.email).execute()
        user = response.data[0] if response.data else None

        # SI ES MODO VIP (SOLO LOGIN)
        if data.login_only:
            if not user:
                return {"status": "error", "analisis_ejecutivo": "El correo no existe en nuestros registros."}
            if str(user.get("password")) != str(data.password):
                return {"status": "error", "analisis_ejecutivo": "Contraseña estratégica incorrecta."}
            
            return {"status": "success"}
        
        # SI ES MODO REGISTRO
        else:
            if user:
                if str(user.get("password")) != str(data.password):
                    return {"status": "error", "analisis_ejecutivo": "El correo ya está registrado con otra contraseña."}
                return {"status": "exists"} # Ya existía y la contraseña coincide
            
            # Si no existe, lo creamos y lo guardamos en Supabase
            nuevo_usuario = {
                "email": data.email,
                "password": data.password,
                "nombre": data.nombre,
                "datos_natales": json.dumps({
                    "fecha": data.fecha,
                    "hora": data.hora,
                    "lugar_original": data.lugar,
                    "lat": data.lat,
                    "lon": data.lon
                }),
                "nivel_suscripcion": "FREE"
            }
            
            supabase.table("clientes_vip").insert(nuevo_usuario).execute()
            return {"status": "success"}
            
    except Exception as e:
        # Si algo falla en Python o Supabase, Vercel recibe el error exacto
        return {"status": "error", "analisis_ejecutivo": f"Fallo en la base de datos: {str(e)}"}


@app.post("/obtener_perfil")
async def obtener_perfil(req: PerfilRequest):
    """
    Ruta para cargar los datos en la Bóveda una vez que el usuario entró
    """
    if not supabase:
        return {"status": "error"}
        
    try:
        response = supabase.table("usuarios").select("*").eq("email", req.email).execute()
        if response.data:
            return {"status": "success", "datos": response.data[0]}
        return {"status": "error"}
    except Exception as e:
        return {"status": "error"}

# Health check para mantener a Render despierto
@app.get("/api/health")
def health():
    return {"status": "online", "system": "VAULT LOGIC ACTIVE"}
