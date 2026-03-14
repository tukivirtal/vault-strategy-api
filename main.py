from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client
import os
import httpx  # Necesario para hablar con MailerLite
from dotenv import load_dotenv

load_dotenv()
supabase: Client = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))
MAILER_KEY = os.environ.get("MAILERLITE_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Ticket(BaseModel):
    email_usuario: str
    plan_nivel: str
    mensaje: str
    estado: str = "ABIERTO"

# Función interna para enviar correos vía MailerLite
async def enviar_notificacion(email_destino, asunto, contenido):
    url_mailer = "https://connect.mailerlite.com/api/emails/transactional"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {MAILER_KEY}"
    }
    data = {
        "to": email_destino,
        "subject": asunto,
        "html": f"<div style='font-family:monospace; background:#000; color:#d4af37; padding:20px;'>{contenido}</div>",
        "from": "GXP System <soporte@emotionalvaults.com>" # Asegúrate que este dominio esté verificado en MailerLite
    }
    async with httpx.AsyncClient() as client:
        await client.post(url_mailer, json=data, headers=headers)

@app.post("/generar_ticket")
async def generar_ticket(ticket: Ticket):
    try:
        import random
        ref = f"GX-{random.randint(10000, 99999)}"
        nombre = ticket.email_usuario.split('@')[0].upper()

        # 1. Guardar en Supabase (Ya funciona)
        data = {
            "ticket_ref": ref,
            "nombre_usuario": nombre,
            "email_usuario": ticket.email_usuario,
            "plan_nivel": ticket.plan_nivel,
            "mensaje": ticket.mensaje,
            "estado": ticket.estado
        }
        supabase.table("soporte_tickets").insert(data).execute()

        # 2. ENVIAR CORREOS DE AVISO (Lo nuevo)
        cuerpo_admin = f"NUEVO TICKET: {ref}<br>Usuario: {nombre}<br>Plan: {ticket.plan_nivel}<br>Mensaje: {ticket.mensaje}"
        cuerpo_usuario = f"Hola {nombre}, tu ticket {ref} ha sido recibido. Nuestro equipo lo revisará bajo protocolo {ticket.plan_nivel}."

        # Aviso a la empresa
        await enviar_notificacion("contact@emotionalvaults.com", f"ALERTA SOPORTE: {ref}", cuerpo_admin)
        # Aviso al cliente
        await enviar_notificacion(ticket.email_usuario, "Confirmación de Ticket GXP", cuerpo_usuario)
        
        return {"status": "success", "ticket_ref": ref}
    
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error en el proceso de notificación")