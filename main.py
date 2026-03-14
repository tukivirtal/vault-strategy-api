from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client
import os
from dotenv import load_dotenv

# 1. Cargar llaves maestras
load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

app = FastAPI()

# 2. Configuración de Seguridad (CORS)
# Esto permite que tu web en Vercel pueda hablar con este servidor en Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, podrías poner aquí tu URL de Vercel
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Modelo de datos para el Ticket
class Ticket(BaseModel):
    email_usuario: str
    plan_nivel: str
    mensaje: str
    estado: str = "ABIERTO"

@app.get("/")
async def root():
    return {"status": "Vault Logic API Operativa", "nucleo": "GXP-2026"}

# 4. Ruta para recibir los tickets de Soporte.html
@app.post("/generar_ticket")
async def generar_ticket(ticket: Ticket):
    try:
        # Generamos una referencia aleatoria GX
        import random
        ref = f"GX-{random.randint(10000, 99999)}"
        nombre = ticket.email_usuario.split('@')[0].upper()

        data = {
            "ticket_ref": ref,
            "nombre_usuario": nombre,
            "email_usuario": ticket.email_usuario,
            "plan_nivel": ticket.plan_nivel,
            "mensaje": ticket.mensaje,
            "estado": ticket.estado
        }

        # Insertar en Supabase
        response = supabase.table("soporte_tickets").insert(data).execute()
        
        return {"status": "success", "ticket_ref": ref}
    
    except Exception as e:
        print(f"Error Crítico: {e}")
        raise HTTPException(status_code=500, detail="Error al indexar ticket en el núcleo")

# Aquí podrías añadir tus rutas de la NASA JPL para Génesis más adelante