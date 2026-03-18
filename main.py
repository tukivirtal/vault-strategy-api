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

# === LAS CLAVES ESTÁN INVISIBLES AQUÍ ===
# Python las lee directamente del entorno de Render, no del código fuente
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if SUPABASE_URL and SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Estructura de datos esperada desde el HTML
class LoginData(BaseModel):
    email: str
    password: str
    login_only: bool = False
    nombre: str = None
    lugar: str = None
    fecha: str = None
    hora: str = None

@app.get("/")
async def read_index():
    return FileResponse('index.html')

@app.post("/consultar")
async def consultar(data: LoginData):
    try:
        if data.login_only:
            # Lógica de Inicio de Sesión
            res = supabase.auth.sign_in_with_password({"email": data.email, "password": data.password})
            return {"status": "success"}
        else:
            # Lógica de Registro
            res = supabase.auth.sign_up({
                "email": data.email,
                "password": data.password,
                "options": {
                    "data": {
                        "nombre": data.nombre,
                        "lugar": data.lugar,
                        "fecha": data.fecha,
                        "hora": data.hora
                    }
                }
            })
            return {"status": "success"}
    except Exception as e:
        # Esto imprimirá el error real en los logs de Render (letras rojas/blancas)
        print(f"🚨 ERROR CRÍTICO DETECTADO: {str(e)}") 
        
        # Esto enviará el error real directamente a tu pantalla de la web
        return {"status": "error", "analisis_ejecutivo": f"Fallo interno: {str(e)}"}
