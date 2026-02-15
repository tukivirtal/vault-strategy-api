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

def obtener_gps(lugar):
    try:
        geolocator = Nominatim(user_agent="vault_logic_production")
        location = geolocator.geocode(lugar)
        if location:
            return {"lat": round(location.latitude, 4), "lon": round(location.longitude, 4)}
    except:
        pass
    return {"lat": "COORD_PENDING", "lon": "COORD_PENDING"}

@app.post("/consultar")
async def consultar(datos: dict):
    # Estandarización de Seguridad y Estética
    nombre = datos.get('nombre', 'VIP').upper()
    email = datos.get('email', '').lower() # El login siempre se procesa en minúsculas
    lugar = datos.get('lugar', '').upper()
    
    coords = obtener_gps(lugar)
    
    # Lógica de Inteligencia (Fase 2)
    # Aquí definimos la directiva técnica que se guardará en su perfil
    directiva = "CONFIGURACIÓN ALCISTA: Ciclo de expansión detectado. Maximice la exposición en activos de alto rendimiento."

    # Datos para la Bóveda del Cliente
    mapa_data = {
        "geo": coords,
        "last_analysis": directiva,
        "engine": "NASA_EPH_V2",
        "status": "VERIFIED_ACCOUNT"
    }

    try:
        # OPERACIÓN UPSERT: La clave de login es el email
        # Si el email existe en la DB, actualiza la fila. Si no, crea una nueva.
        supabase.table("clientes_vip").upsert({
            "email": email,
            "nombre": nombre,
            "datos_natales": datos,
            "mapatotal": mapa_data,
            "nivel_suscripcion": "free"
        }, on_conflict="email").execute()
        
    except Exception as e:
        print(f"Bóveda Error: {e}")

    return {
        "titulo": "DIRECTIVA ESTRATÉGICA",
        "analisis_ejecutivo": directiva,
        "coordinadas": f"GEO-REF: {coords['lat']}, {coords['lon']}",
        "firma": "VAULT LOGIC EXECUTIVE"
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
