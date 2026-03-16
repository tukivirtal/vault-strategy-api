from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client
import os
import httpx
from dotenv import load_dotenv
from typing import Optional
from datetime import date, timedelta
import random

load_dotenv()

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    print("ADVERTENCIA: Las variables de entorno de Supabase no están configuradas. El API usará datos de marcador de posición.")
    supabase = None
else:
    supabase: Client = create_client(supabase_url, supabase_key)

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

# ... (resto de las rutas de la API como /generar_ticket, etc.)

@app.get("/api/stats")
async def get_stats(start_date: date, end_date: date):
    try:
        num_days = max(1, (end_date - start_date).days + 1)
        chart_labels = [(start_date + timedelta(days=i)).strftime('%a %d') for i in range(num_days)]
        chart_data = [random.randint(20, 150) for _ in range(num_days)]

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
    except Exception as e:
        print(f"Error CRÍTICO en /api/stats: {e}")
        num_days = max(1, (end_date - start_date).days + 1)
        default_categories = [(start_date + timedelta(days=i)).strftime('%a %d') for i in range(num_days)]
        return {
            "capital_gxp": 0.0,
            "negociacion": 0.0,
            "riesgo": 0.0,
            "chart": {
                "series": [{"name": "Sincronía GXP", "data": [0] * len(default_categories)}],
                "xaxis": {"categories": default_categories}
            }
        }

@app.get("/")
async def read_index():
    return FileResponse('genesis-live.html')

# Ruta genérica para servir otros archivos HTML
@app.get("/{file_path:path}")
async def serve_static_html(file_path: str):
    # Por seguridad, solo permitir archivos .html
    if file_path.endswith('.html'):
        if os.path.exists(file_path):
            return FileResponse(file_path)
    return Response(status_code=404)
