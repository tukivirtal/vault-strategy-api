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
    """Sincronización en dos pasos: Datos -> Grupo"""
    if not MAILERLITE_API_KEY:
        print("Error: API Key de MailerLite no encontrada")
        return

    email_limpio = email.strip().lower()
    headers = {
        "Authorization": f"Bearer {MAILERLITE_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # PASO 1: Crear/Actualizar los datos del suscriptor en la lista general
    url_sub = "https://connect.mailerlite.com/api/subscribers"
    payload_sub = {
        "email": email_limpio,
        "fields": {
            "name": nombre,
            "vl_nombre": nombre,
            "vl_directiva": directiva,
            "vl_geo_ref": f"{coords['lat']}, {coords['lon']}"
        }
    }

    async with httpx.AsyncClient() as client:
        try:
            # Aseguramos los datos básicos
            res_sub = await client.post(url_sub, headers=headers, json=payload_sub, timeout=15.0)
            
            # PASO 2: Forzar la entrada al grupo específico de Vault Logic
            if res_sub.status_code in [200, 201, 204]:
                grupo_id = 17952042256303511 
                url_grupo = f"https://connect.mailerlite.com/api/groups/{grupo_id}/subscribers"
                
                # Enviamos el email al endpoint del grupo para disparar automatizaciones
                res_g = await client.post(url_grupo, headers=headers, json={"email": email_limpio}, timeout=15.0)
                print(f"Sincronización completa: {email_limpio}. Resultado Grupo: {res_g.status_code}")
            else:
                print(f"Error al crear suscriptor: {res_sub.status_code} - {res_sub.text}")
        except Exception as e:
            print(f"Fallo crítico en sincronización: {e}")

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
