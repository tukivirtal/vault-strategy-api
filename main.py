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
    # 1. Limpieza y Validación de Entradas
    email = datos.get('email', '').strip().lower()
    nombre = datos.get('nombre', 'VIP MEMBER').strip().upper()
    if not nombre: nombre = "VIP MEMBER"

    lugar = datos.get('lugar', '').strip().upper()
    hora = datos.get('hora', '12:00')
    if not hora: hora = "12:00"

    # 2. BLOQUE DE SEGURIDAD: Verificar si el usuario ya existe
    try:
        # Buscamos el email en la tabla antes de hacer nada más
        check_user = supabase.table("clientes_vip").select("email").eq("email", email).execute()
        
        if check_user.data:
            # Si el email existe, enviamos una respuesta de advertencia
            return {
                "status": "exists",
                "titulo": "ACCESO PREVIAMENTE REGISTRADO",
                "analisis_ejecutivo": "Tu email ya se encuentra en nuestra base de datos estratégica. Revisa tu bandeja de entrada o contacta a soporte para recuperar tu acceso.",
                "coordinadas": "SISTEMA BLOQUEADO: USUARIO EXISTENTE",
                "firma": "VAULT LOGIC SECURITY"
            }
    except Exception as e:
        print(f"Error al verificar duplicado en Supabase: {e}")

    # 3. Si el usuario es nuevo, procedemos con la geolocalización
    coords = obtener_gps(lugar)

    # 4. Directiva Estratégica
    directiva = "NODO DE EXPANSIÓN ACTIVO: Sincronía detectada. Momento óptimo para la ejecución de protocolos de crecimiento."

    # 5. Guardado en Supabase (Bóveda)
    try:
        # Aquí usamos upsert con on_conflict pero ya sabemos que es nuevo o falló el check
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

    # 6. Sincronización con MailerLite
    try:
        await sincronizar_mailerlite(email, nombre, directiva, coords)
    except Exception as e:
        print(f"Error Crítico MailerLite: {e}")

    return {
        "status": "success",
        "titulo": "DIRECTIVA ESTRATÉGICA GENERADA",
        "analisis_ejecutivo": directiva,
        "coordinadas": f"GEO-REF: {coords['lat']}, {coords['lon']}",
        "firma": "VAULT LOGIC EXECUTIVE"
    }
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
