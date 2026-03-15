from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client
import os
import httpx
from dotenv import load_dotenv
from typing import Optional
from datetime import date
import random

load_dotenv()
supabase: Client = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))

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

async def add_subscriber_to_mailerlite(email, fields):
    url_mailer = "https://connect.mailerlite.com/api/subscribers"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ.get('MAILERLITE_API_KEY')}"
    }
    group_id_str = os.environ.get('MAILERLITE_GROUP_ID')
    group_id = int(group_id_str) if group_id_str else None
    data = {
        "email": email,
        "fields": fields,
        "groups": [group_id] if group_id else []
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url_mailer, json=data, headers=headers)
        if response.status_code not in [200, 201]:
            print(f'ERROR CRÍTICO MAILERLITE: {response.status_code} - {response.text}')

@app.post("/generar_ticket")
async def generar_ticket(ticket: Ticket):
    try:
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
        supabase.table("soporte_tickets").insert(data).execute()
        mailerlite_fields = {
            "ticket_ref": ref,
            "plan_nivel": ticket.plan_nivel
        }
        await add_subscriber_to_mailerlite(ticket.email_usuario, mailerlite_fields)
        return {"status": "success", "ticket_ref": ref}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error en el proceso de notificación")

@app.get("/api/stats")
async def get_stats(start_date: date, end_date: date):
    # Lógica de marcador de posición para la consulta de la base de datos
    # Aquí es donde se consultaría a Supabase
    chart_data = [random.randint(20, 150) for _ in range(7)]
    chart_labels = ['Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab', 'Dom']
    
    capital_gxp_pct = round(random.uniform(-25, 50), 1)
    negociacion_pct = round(random.uniform(-15, 30), 1)
    riesgo_pct = round(random.uniform(-50, 0), 1)

    return {
        "capital_gxp": capital_gxp_pct,
        "negociacion": negociacion_pct,
        "riesgo": riesgo_pct,
        "chart": {
            "series": [{"name": "Sincronía GXP", "data": chart_data}],
            "xaxis": {"categories": chart_labels}
        }
    }

# Force Render deploy
