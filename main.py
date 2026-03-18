from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from supabase import create_client, Client

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# === LAS CLAVES SIGUEN INVISIBLES Y SEGURAS AQUÍ ===
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if SUPABASE_URL and SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class LoginData(BaseModel):
    email: str
    password: str
    login_only: bool = False
    nombre: str = None
    lugar: str = None
    fecha: str = None
    hora: str = None

class PerfilRequest(BaseModel):
    email: str

@app.get("/")
async def read_index():
    return FileResponse('index.html')

@app.post("/consultar")
async def consultar(data: LoginData):
    try:
        if data.login_only:
            # Buscamos en tu tabla 'clientes_vip', NO en el sistema Auth
            res = supabase.table("clientes_vip").select("*").eq("email", data.email).execute()
            
            if len(res.data) > 0:
                usuario = res.data[0]
                
                # Verificamos la contraseña
                if "password" in usuario and str(usuario["password"]) != str(data.password):
                    return {"status": "error", "analisis_ejecutivo": "Contraseña estratégica incorrecta."}
                
                # === ENRUTAMIENTO INTELIGENTE ===
                # Extraemos el plan. Si no tiene, se le asigna 'free' por defecto.
                suscripcion = usuario.get("nivel_suscripcion", "free")
                
                return {"status": "success", "nivel_suscripcion": suscripcion}
            else:
                return {"status": "error", "analisis_ejecutivo": "El email no se encuentra en la base de datos VIP."}
        
        else:
            # Lógica de Registro
            nuevo_usuario = {
                "email": data.email,
                "password": data.password, 
                "nombre": data.nombre,
                "datos_natales": {
                    "fecha": data.fecha,
                    "hora": data.hora,
                    "lugar_original": data.lugar
                },
                "nivel_suscripcion": "free"
            }
            supabase.table("clientes_vip").insert(nuevo_usuario).execute()
            
            # Al registrarse, por defecto es free
            return {"status": "success", "nivel_suscripcion": "free"}
            
    except Exception as e:
        print(f"🚨 ERROR CRÍTICO DETECTADO: {str(e)}")
        return {"status": "error", "analisis_ejecutivo": f"Fallo en la tabla: {str(e)}"}

# === NUEVA RUTA PARA REVIVIR BOVEDA.HTML ===
@app.post("/obtener_perfil")
async def obtener_perfil(req: PerfilRequest):
    try:
        res = supabase.table("clientes_vip").select("*").eq("email", req.email).execute()
        if len(res.data) > 0:
            return {"status": "success", "datos": res.data[0]}
        else:
            return {"status": "error", "mensaje": "Datos no encontrados"}
    except Exception as e:
        print(f"🚨 ERROR EN PERFIL: {str(e)}")
        return {"status": "error", "mensaje": "Fallo de conexión al núcleo"}
