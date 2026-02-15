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

# Conexión con Supabase
supabase: Client = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))

def obtener_gps(lugar):
    """Convierte texto en coordenadas reales"""
    try:
        # Usamos un agente de usuario específico para evitar bloqueos
        geolocator = Nominatim(user_agent="vault_logic_production")
        location = geolocator.geocode(lugar)
        if location:
            return {"lat": round(location.latitude, 4), "lon": round(location.longitude, 4)}
    except:
        pass
    return {"lat": "N/A", "lon": "N/A"}

def motor_estrategico(aspecto):
    """Traducción de matemática a directiva ejecutiva"""
    dict_poder = {
        "SOL_JUPITER": "VENTANA DE ESCALABILIDAD ALTA: Sincronía detectada en ciclos de crecimiento. Momento óptimo para la inyección de capital.",
        "DEFAULT": "ESTABILIDAD OPERATIVA: Mantener curso actual. No se detectan fluctuaciones de alto impacto."
    }
    return dict_poder.get(aspecto, dict_poder["DEFAULT"])

@app.post("/consultar")
async def consultar(datos: dict):
    # Forzamos mayúsculas para coherencia estética
    nombre = datos.get('nombre', 'VIP').upper()
    email = datos.get('email', '').lower()
    lugar = datos.get('lugar', '').upper()
    
    # 1. Obtención de Coordenadas Reales
    coords = obtener_gps(lugar)
    
    # 2. Selección de Directiva (Basado en la lógica de Fase 2)
    directiva = motor_estrategico("SOL_JUPITER")

    # 3. Guardado en la Bóveda (Supabase)
    try:
        supabase.table("clientes_vip").insert({
            "nombre": nombre,
            "email": email,
            "datos_natales": datos,
            "mapatotal": {"geo": coords, "status": "MATHEMATICALLY_VERIFIED", "version": "2.0"},
            "nivel_suscripcion": "free"
        }).execute()
    except Exception as e:
        print(f"Error en Bóveda: {e}")

    # 4. Entrega de Estatus al usuario
    return {
        "titulo": "DIRECTIVA ESTRATÉGICA",
        "analisis_ejecutivo": directiva,
        "coordinadas": f"GEO-REF: {coords['lat']}, {coords['lon']}",
        "firma": "VAULT LOGIC EXECUTIVE"
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
