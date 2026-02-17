from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from geopy.geocoders import Nominatim
import os
import uvicorn
import httpx

app = FastAPI()

# Configuración de CORS
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
    """Envía el prospecto a MailerLite con las etiquetas corregidas"""
    if not MAILERLITE_API_KEY:
        return

    # Limpieza de seguridad
    email_limpio = email.strip().lower()
    
    url = "https://connect.mailerlite.com/api/subscribers"
    headers = {
        "Authorization": f"Bearer {MAILERLITE_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # Payload para crear/actualizar suscriptor
    payload = {
        "email": email_limpio,
        "fields": {
            "name": nombre,
            "vl_nombre": nombre,
            "vl_directiva": directiva,
            "vl_geo_ref": f"{coords['lat']}, {coords['lon']}"
        }
    }

    async with httpx.AsyncClient() as client:
        # 1. Crear o actualizar el suscriptor
        response = await client.post(url, headers=headers, json=payload, timeout=10.0)
        
        # 2. Si tuvo éxito, forzar su entrada al grupo de Vault Logic
        if response.status_code in [200, 201]:
            grupo_id = 17952042256303511
            # Corregido: Ahora usamos f-string real para inyectar las variables en la URL
            url_grupo = f"https://connect.mailerlite.com/api/subscribers/{email_limpio}/groups/{grupo_id}"
            await client.post(url_grupo, headers=headers, timeout=10.0)
            print(f"Sincronización completa para: {email_limpio}")

@app.post("/consultar")
async def consultar(datos: dict):
    # 1. Limpieza y Validación de Entradas
    nombre = datos.get('nombre', 'VIP MEMBER').strip().upper()
    if not nombre: nombre = "VIP MEMBER"

    email = datos.get('email', '').strip().lower()
    lugar = datos.get('lugar', '').strip().upper()
    hora = datos.get('hora', '12:00')
    if not hora: hora = "12:00"

    # 2. Geolocalización
    coords = obtener_gps(lugar)

    # 3. Directiva Estratégica
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
