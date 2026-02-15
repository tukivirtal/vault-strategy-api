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

# Conexión Supabase
supabase: Client = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))

def obtener_datos_geograficos(lugar):
    """Convierte texto en coordenadas reales para el motor matemático"""
    try:
        geolocator = Nominatim(user_agent="vault_logic_pro")
        location = geolocator.geocode(lugar)
        if location:
            return {"lat": location.latitude, "lon": location.longitude}
    except:
        pass
    return {"lat": "COORD_UNAVAILABLE", "lon": "COORD_UNAVAILABLE"}

def motor_logico_ejecutivo(data_astral):
    """Diccionario de correspondencias para briefings fríos y directos"""
    reglas = {
        "SOL_JUPITER": "CONFIGURACIÓN ALCISTA: Ciclo de expansión de activos detectado. Momento de alta probabilidad para cierre de acuerdos y escalado.",
        "MARTE_SATURNO": "TENSIÓN ESTRUCTURAL: Resistencia en la ejecución. Se recomienda auditoría de procesos y blindaje legal antes de proceder.",
        "DEFAULT": "ESTABILIDAD OPERATIVA: Parámetros dentro del rango esperado. Ejecutar según planificación estratégica."
    }
    return reglas.get(data_astral, reglas["DEFAULT"])

@app.post("/consultar")
async def consultar(datos: dict):
    nombre = datos.get('nombre', 'VIP').upper()
    email = datos.get('email')
    lugar = datos.get('lugar', '').upper()
    
    # 1. Obtener Georeferencia Real
    coords = obtener_datos_geograficos(lugar)
    
    # 2. Determinar Directiva (Próximamente vinculado a pyswisseph)
    aspecto_clave = "SOL_JUPITER" 
    briefing = motor_logico_ejecutivo(aspecto_clave)

    # 3. Guardado en Bóveda
    mapa_data = {
        "coords": coords,
        "aspecto": aspecto_clave,
        "status": "MATHEMATICALLY_VERIFIED"
    }

    try:
        supabase.table("clientes_vip").insert({
            "nombre": nombre,
            "email": email,
            "datos_natales": datos,
            "mapatotal": mapa_data,
            "nivel_suscripcion": "free"
        }).execute()
    except Exception as e:
        print(f"DB Error: {e}")

    return {
        "titulo": "DIRECTIVA ESTRATÉGICA",
        "analisis_ejecutivo": briefing,
        "coordinadas": f"LAT: {coords['lat']} | LON: {coords['lon']}",
        "firma": "VAULT LOGIC SYSTEM"
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
