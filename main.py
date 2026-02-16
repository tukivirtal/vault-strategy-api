from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from geopy.geocoders import Nominatim
import os
import uvicorn
import httpx

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Credenciales de Entorno
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
MAILERLITE_API_KEY = os.environ.get("MAILERLITE_API_KEY") 

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def obtener_gps(lugar):
    """Geolocalización real para validación matemática"""
    try:
        geolocator = Nominatim(user_agent="vault_logic_pro")
        location = geolocator.geocode(lugar)
        if location:
            return {"lat": round(location.latitude, 4), "lon": round(location.longitude, 4)}
    except:
        pass
    return {"lat": "COORD_PENDING", "lon": "COORD_PENDING"}

async def sincronizar_mailerlite(email, nombre, directiva, coords):
    """Envía el prospecto a MailerLite para el flujo de bienvenida"""
    if not MAILERLITE_API_KEY: return
    
    url = "https://connect.mailerlite.com/api/subscribers"
    headers = {
        "Authorization": f"Bearer {MAILERLITE_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
 payload = {
        "email": email,
        "fields": {
            "name": nombre,
            "vl_directiva": directiva,
            "vl_geo_ref": f"{coords['lat']}, {coords['lon']}"
        }
    }
    async with httpx.AsyncClient() as client:
        await client.post(url, headers=headers, json=payload)

@app.post("/consultar")
async def consultar(datos: dict):
    # Procesamiento Ejecutivo
    nombre = datos.get('nombre', 'VIP MEMBER').upper()
    email = datos.get('email', '').lower()
    lugar = datos.get('lugar', '').upper()
    
    # 1. Cálculo Geográfico Real
    coords = obtener_gps(lugar)
    
    # 2. Directiva Estratégica (Lógica de Fase 2)
    directiva = "NODO DE EXPANSIÓN ACTIVO: Sincronía detectada en ciclos de crecimiento. Momento óptimo para la inyección de capital."

    # 3. Guardado en Supabase (UPSERT para evitar duplicados)
    try:
        supabase.table("clientes_vip").upsert({
            "email": email,
            "nombre": nombre,
            "datos_natales": datos,
            "mapatotal": {"geo": coords, "directive": directiva, "auth": "VERIFIED_VAULT"},
            "nivel_suscripcion": "free"
        }, on_conflict="email").execute()
    except Exception as e:
        print(f"Error Bóveda: {e}")

    # 4. Sincronización con MailerLite
    await sincronizar_mailerlite(email, nombre, directiva, coords)

    return {
        "titulo": "DIRECTIVA ESTRATÉGICA GENERADA",
        "analisis_ejecutivo": directiva,
        "coordinadas": f"GEO-REF: {coords['lat']}, {coords['lon']}",
        "firma": "VAULT LOGIC EXECUTIVE"
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
