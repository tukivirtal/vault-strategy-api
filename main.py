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

@app.get("/api/stats")
async def get_stats(start_date: date, end_date: date):
    if not supabase:
        # Fallback to placeholder data if Supabase is not connected
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

    try:
        # Fetch data from Supabase
        query_result = supabase.table('gxp_metrics').select('fecha', 'sincronia_gxp', 'capital_gxp', 'negociacion', 'riesgo').gte('fecha', start_date).lte('fecha', end_date).order('fecha').execute()
        
        if not query_result.data:
            raise HTTPException(status_code=404, detail="No se encontraron datos para el rango de fechas especificado.")

        data = query_result.data
        
        # Process data for the frontend
        chart_labels = [item['fecha'] for item in data]
        chart_data = [item['sincronia_gxp'] for item in data]
        
        # Calculate averages for the KPIs, handle potential division by zero
        num_records = len(data)
        capital_gxp_avg = round(sum(d['capital_gxp'] for d in data) / num_records, 1) if num_records > 0 else 0
        negociacion_avg = round(sum(d['negociacion'] for d in data) / num_records, 1) if num_records > 0 else 0
        riesgo_avg = round(sum(d['riesgo'] for d in data) / num_records, 1) if num_records > 0 else 0

        return {
            "capital_gxp": capital_gxp_avg,
            "negociacion": negociacion_avg,
            "riesgo": riesgo_avg,
            "chart": {
                "series": [{"name": "Sincronía GXP", "data": chart_data}],
                "xaxis": {"categories": chart_labels}
            }
        }

    except Exception as e:
        print(f"Error CRÍTICO en /api/stats: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor al procesar las estadísticas.")

@app.get("/")
async def read_index():
    return FileResponse('genesis-live.html')

@app.get("/{file_path:path}")
async def serve_static_html(file_path: str):
    if file_path.endswith('.html'):
        if os.path.exists(file_path):
            return FileResponse(file_path)
    return Response(status_code=404)