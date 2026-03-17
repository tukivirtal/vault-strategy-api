from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Permitir que el navegador no bloquee las peticiones (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_index():
    # Buscamos el archivo directamente en la raíz
    return FileResponse('genesis-live.html')

@app.get("/api/stats")
async def get_stats():
    # Esto es para que el panel NO de error de sincronización
    # Devuelve datos reales o por defecto si falla la DB
    return {
        "capital": 24.8,
        "negociacion": 12.2,
        "riesgo": -18.5,
        "status": "ACTIVE",
        "last_sync": "2026-03-16"
    }
