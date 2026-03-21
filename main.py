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
    lat: str = None
    lon: str = None

class PerfilRequest(BaseModel):
    email: str

@app.get("/")
async def read_index():
    return FileResponse('index.html')

@app.post("/api/consultar")
async def consultar(data: LoginData):
    try:
        if data.login_only:
            # === MODO VIP (LOGIN) ===
            res = supabase.table("clientes_vip").select("*").eq("email", data.email).execute()
            
            if len(res.data) > 0:
                usuario = res.data[0]
                
                # Verificamos la contraseña
                if "password" in usuario and str(usuario["password"]) != str(data.password):
                    return {"status": "error", "analisis_ejecutivo": "Contraseña estratégica incorrecta."}
                
                # Extraemos el plan. Si no tiene, se le asigna 'free'
                suscripcion = usuario.get("nivel_suscripcion", "free")
                
                # AQUÍ ESTÁ LA MAGIA DEL NOMBRE:
                # Extraemos el nombre de la BD y se lo pasamos al navegador
                nombre_usuario = usuario.get("nombre", "OPERADOR GXP")
                
                return {
                    "status": "success", 
                    "nivel_suscripcion": suscripcion,
                    "nombre": nombre_usuario
                }
            else:
                return {"status": "error", "analisis_ejecutivo": "El email no se encuentra en la base de datos VIP."}
        
        else:
            # === MODO NUEVA TERMINAL (REGISTRO) ===
            nuevo_usuario = {
                "email": data.email,
                "password": data.password, 
                "nombre": data.nombre,
                "datos_natales": {
                    "fecha": data.fecha,
                    "hora": data.hora,
                    "lugar_original": data.lugar,
                    "lat": data.lat,  
                    "lon": data.lon   
                },
                "nivel_suscripcion": "free"
            }
            supabase.table("clientes_vip").insert(nuevo_usuario).execute()
            
            # Al registrarse, el navegador ya tiene el nombre que el usuario escribió, 
            # pero por las dudas también se lo enviamos limpio.
            return {
                "status": "success", 
                "nivel_suscripcion": "free",
                "nombre": data.nombre
            }
            
    except Exception as e:
        print(f"🚨 ERROR CRÍTICO DETECTADO: {str(e)}")
        return {"status": "error", "analisis_ejecutivo": f"Fallo en el núcleo: {str(e)}"}

# === NUEVA RUTA PARA REVIVIR BOVEDA.HTML ===
@app.post("/api/obtener_perfil")
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
