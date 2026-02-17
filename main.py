from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from geopy.geocoders import Nominatim
import os
import uvicorn
import httpx

app = FastAPI()

# Configuración de CORS - Permitir conexiones desde tu web en Vercel
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

    url = "https://connect.mailerlite.com/api/subscribers"
    headers = {
        "Authorization": f"Bearer {MAILERLITE_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

  payload = {
        "email": email,
        "fields": {
            "name": nombre,           # Mantenemos este por si acaso
            "vl_nombre": nombre,      # Esta es la que usará tu diseño {$vl_nombre}
            "vl_directiva": directiva,
            "vl_geo_ref": f"{coords['lat']}, {coords['lon']}"
        }
    }

    async with httpx.AsyncClient() as client:
        await client.post(url, headers=headers, json=payload)

@app.post("/consultar")
async def consultar(datos: dict):
    # 1. Limpieza y Validación de Entradas (Evita errores si el campo viene vacío)
    nombre = datos.get('nombre', 'VIP MEMBER').strip().upper()
    if not nombre: nombre = "VIP MEMBER"
    
    email = datos.get('email', '').strip().lower()
    lugar = datos.get('lugar', '').strip().upper()
    hora = datos.get('hora', '12:00') # Si no sabe la hora, usamos mediodía por defecto
    if not hora: hora = "12:00"

    # 2. Gestión inteligente de la ubicación (El tema de la coma)
    # Si no puso coma, intentamos buscarlo igual; si falla, usamos el paracaídas.
    coords = obtener_gps(lugar)
    
    # 3. Directiva Estratégica
    # Aquí es donde el sistema "decide" qué decir según los datos.
    directiva = "NODO DE EXPANSIÓN ACTIVO: Sincronía detectada. Momento óptimo para la ejecución de protocolos de crecimiento."

    # 4. Guardado en Supabase (Bóveda)
    # Incluimos la hora y el lugar original para que tú lo veas en el admin
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
    # Enviamos los datos limpios para que el mail no llegue vacío
    try:
        await sincronizar_mailerlite(email, nombre, directiva, coords)
    except Exception as e:
        print(f"Error MailerLite: {e}")

    return {
        "titulo": "DIRECTIVA ESTRATÉGICA GENERADA",
        "analisis_ejecutivo": directiva,
        "coordinadas": f"GEO-REF: {coords['lat']}, {coords['lon']}",
        "firma": "VAULT LOGIC EXECUTIVE"
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
