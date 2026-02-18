from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from geopy.geocoders import Nominatim
import os
import uvicorn
import httpx

app = FastAPI()

# Configuración de CORS - Permitir todas para facilitar la conexión con Vercel
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

# Inicialización de Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def obtener_gps(lugar):
    """Geolocalización real para validación técnica"""
    try:
        geolocator = Nominatim(user_agent="vault_logic_pro")
        location = geolocator.geocode(lugar)
        if location:
            return {"lat": round(location.latitude, 4), "lon": round(location.longitude, 4)}
    except:
        pass
    return {"lat": "COORD_PENDING", "lon": "COORD_PENDING"}

async def sincronizar_mailerlite(email, nombre, directiva, coords):
    """Versión simplificada y directa para forzar la entrada al grupo"""
    if not MAILERLITE_API_KEY: return

    email_limpio = email.strip().lower()
    headers = {
        "Authorization": f"Bearer {MAILERLITE_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # PASO ÚNICO: Crear/Actualizar y asignar grupo en una sola instrucción
    url = "https://connect.mailerlite.com/api/subscribers"
    payload = {
        "email": email_limpio,
        "fields": {
            "name": nombre,
            "vl_nombre": nombre,
            "vl_directiva": directiva,
            "vl_geo_ref": f"{coords['lat']}, {coords['lon']}"
        },
        "groups": ["179520042256303511"] # Reemplaza con tu ID de grupo real
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=payload, timeout=15.0)
            print(f"Respuesta MailerLite para {email_limpio}: {response.status_code}")
            if response.status_code not in [200, 201]:
                print(f"Detalle del error: {response.text}")
        except Exception as e:
            print(f"Error de conexión: {e}")

@app.post("/consultar")
async def consultar(datos: dict):
    # 1. Limpieza y Validación de Entradas (Stress Test Proof)
    nombre = datos.get('nombre', 'VIP MEMBER').strip().upper()
    if not nombre: nombre = "VIP MEMBER"

    email = datos.get('email', '').strip().lower()
    lugar = datos.get('lugar', '').strip().upper()
    hora = datos.get('hora', '12:00')
    if not hora: hora = "12:00"

    # 2. Geolocalización automática
    coords = obtener_gps(lugar)

    # 3. Directiva Estratégica (Comentario fijo por ahora)
    directiva = "NODO DE EXPANSIÓN ACTIVO: Sincronía detectada. Momento óptimo para la ejecución de protocolos de crecimiento."

    # 4. Guardado en Supabase (Bóveda)
    try:
        supabase.table("clientes_vip").upsert({
            "email": email,
            "nombre": nombre,
            "datos_natales": {
                "lugar_original": lugar,
                "hora_nacimiento": hora,
                "fecha": datos.get('fecha', 'SIN_FECHA')
            },
            "mapatotal": {
                "geo": coords, 
                "directive": directiva, 
                "auth": "VERIFIED_VAULT"
            },
            "nivel_suscripcion": "free"
        }, on_conflict="email").execute()
    except Exception as e:
        print(f"Error Bóveda Supabase: {e}")

    # 5. Sincronización con MailerLite
    try:
        await sincronizar_mailerlite(email, nombre, directiva, coords)
    except Exception as e:
        print(f"Error Crítico MailerLite: {e}")

    return {
        "titulo": "DIRECTIVA ESTRATÉGICA GENERADA",
        "analisis_ejecutivo": directiva,
        "coordinadas": f"GEO-REF: {coords['lat']}, {coords['lon']}",
        "firma": "VAULT LOGIC EXECUTIVE"
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
