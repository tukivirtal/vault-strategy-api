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
    """Sincronización en dos pasos: Datos -> Grupo"""
    if not MAILERLITE_API_KEY:
        return

    email_limpio = email.strip().lower()
    headers = {
        "Authorization": f"Bearer {MAILERLITE_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

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
            res_sub = await client.post(url_sub, headers=headers, json=payload_sub, timeout=15.0)
            if res_sub.status_code in [200, 201, 204]:
                grupo_id = 17952042256303511 
                url_grupo = f"https://connect.mailerlite.com/api/groups/{grupo_id}/subscribers"
                await client.post(url_grupo, headers=headers, json={"email": email_limpio}, timeout=15.0)
        except Exception as e:
            print(f"Error MailerLite: {e}")
import swisseph as swe
from datetime import datetime

def calcular_vectores_natales(fecha_str, hora_str, coords):
    """
    Transforma datos de tiempo y espacio en coordenadas eclípticas exactas.
    Utiliza el motor de Efemérides Suizas.
    """
    # 1. Configurar fecha y hora UT (Tiempo Universal)
    # Por ahora asumimos una zona horaria estándar, luego la haremos dinámica
    fecha_dt = datetime.strptime(fecha_str, "%Y-%m-%d")
    hora_dt = datetime.strptime(hora_str, "%H:%M")
    
    # Convertir a Julian Day (formato matemático de tiempo astronómico)
    jd = swe.julday(fecha_dt.year, fecha_dt.month, fecha_dt.day, 
                    hora_dt.hour + hora_dt.minute/60.0)

    # 2. Lista de puntos de datos a analizar (Sol, Luna, Mercurio, etc.)
    puntos_interes = {
        "SOL": swe.SUN, "LUNA": swe.MOON, "MERCURIO": swe.MERCURY, 
        "VENUS": swe.VENUS, "MARTE": swe.MARS, "JUPITER": swe.JUPITER, 
        "SATURNO": swe.SATURN
    }

    vectores = {}
    for nombre, codigo in puntos_interes.items():
        res = swe.calc_ut(jd, codigo)
        # res[0] es la longitud exacta en el círculo de 360°
        vectores[nombre] = round(res[0], 4)

    return vectores

@app.post("/consultar")
async def consultar(datos: dict):
    # 1. Limpieza de Entradas
    email = datos.get('email', '').strip().lower()
    nombre = datos.get('nombre', 'VIP MEMBER').strip().upper()
    if not nombre: nombre = "VIP MEMBER"
    lugar = datos.get('lugar', '').strip().upper()
    hora = datos.get('hora', '12:00')
    if not hora: hora = "12:00"

    # 2. Verificar duplicado
    try:
        check_user = supabase.table("clientes_vip").select("email").eq("email", email).execute()
        if check_user.data:
            return {
                "status": "exists",
                "titulo": "ACCESO PREVIAMENTE REGISTRADO",
                "analisis_ejecutivo": "Tu email ya se encuentra en nuestra base de datos estratégica.",
                "coordinadas": "SISTEMA BLOQUEADO: USUARIO EXISTENTE",
                "firma": "VAULT LOGIC SECURITY"
            }
    except Exception as e:
        print(f"Error Check: {e}")

    # 3. Procesar Nuevo
    coords = obtener_gps(lugar)
    directiva = "NODO DE EXPANSIÓN ACTIVO: Sincronía detectada. Momento óptimo para la ejecución de protocolos de crecimiento."

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
        print(f"Error Supabase: {e}")

    await sincronizar_mailerlite(email, nombre, directiva, coords)

    return {
        "status": "success",
        "titulo": "DIRECTIVA ESTRATÉGICA GENERADA",
        "analisis_ejecutivo": directiva,
        "coordinadas": f"GEO-REF: {coords['lat']}, {coords['lon']}",
        "firma": "VAULT LOGIC EXECUTIVE"
    }

@app.get("/obtener_reporte/{email}")
async def obtener_reporte(email: str):
    """Endpoint para la Bóveda dinámica"""
    try:
        email_limpio = email.strip().lower()
        resultado = supabase.table("clientes_vip").select("*").eq("email", email_limpio).execute()
        
        if not resultado.data:
            return {"status": "error", "message": "Firma no encontrada."}
            
        user = resultado.data[0]
        return {
            "status": "success",
            "data": {
                "nombre": user['nombre'],
                "directiva": user['mapatotal']['directive'],
                "geo_ref": f"LAT: {user['mapatotal']['geo']['lat']} | LON: {user['mapatotal']['geo']['lon']}",
                "fecha": user['datos_natales']['fecha'],
                "hora": user['datos_natales']['hora_nacimiento'],
                "lugar": user['datos_natales']['lugar_original'],
                "auth_code": user['mapatotal']['auth']
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
