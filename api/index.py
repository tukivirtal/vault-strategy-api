# api/index.py
from fastapi import FastAPI
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

@app.post("/api/consultar") # Cambiamos la ruta para que empiece por /api
async def consultar(data: LoginData):
    # ... (tu lógica de Supabase igual que antes)
    # Asegúrate de mantener el mismo código de antes aquí dentro
    pass

@app.post("/api/obtener_perfil") # Cambiamos la ruta
async def obtener_perfil(req: BaseModel): # Ajusta según tu necesidad
    # ... (tu lógica de perfil igual que antes)
    pass
