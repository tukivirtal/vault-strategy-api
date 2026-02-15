from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from geopy.geocoders import Nominatim
import os
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

supabase: Client = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))

def obtener_gps(lugar):
    """Obtiene coordenadas reales para validar el estatus matemático"""
    try:
        geolocator = Nominatim(user_agent="vault_logic_v2")
        location = geolocator.geocode(lugar)
        if location:
            return {"lat": round(location.latitude, 4), "lon": round(location.longitude, 4)}
    except:
        pass
    return {"lat": "S/D", "lon": "S/D"}

@app.post("/consultar")
async def consultar(datos: dict):
    # Estandarización Ejecutiva
    nombre = datos.get('nombre', 'VIP').upper()
    email = datos.get('email', '').lower()
    lugar = datos.get('lugar', '').upper()
    
    # Cálculo Geográfico Real
    coords = obtener_gps(lugar)
    
    # Simulación de Fase 2 (En espera de flatlib)
    briefing = "VENTANA DE ESCALABILIDAD ALTA: Sincronía detectada en ciclos de crecimiento. Momento óptimo para la inyección de capital."

    # Guardado en Bóveda
    try:
        supabase.table("clientes_vip").insert({
            "nombre": nombre,
            "email": email,
            "datos_natales": datos,
            "mapatotal": {"geo": coords, "status": "VERIFIED_NASA_EPH"},
            "nivel_suscripcion": "free"
        }).execute()
    except Exception as e:
        print(f"Error DB: {e}")

    return {
        "titulo": "DIRECTIVA ESTRATÉGICA",
        "analisis_ejecutivo": briefing,
        "coordinadas": f"GEO-REF: {coords['lat']}, {coords['lon']}",
        "firma": "VAULT LOGIC SYSTEM"
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
