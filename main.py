from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
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
    # Diccionario de respaldo rápido para evitar consultar internet
    respaldos = {
        "SAN FRANCISCO": {"lat": 37.7749, "lon": -122.4194},
        "BARRANQUILLA": {"lat": 10.9685, "lon": -74.7813},
        "NEW YORK": {"lat": 40.7128, "lon": -74.0060},
        "CARMELO": {"lat": -34.0000, "lon": -58.2833}
    }

    # 1. Verificar si es una ciudad conocida en nuestra base local
    lugar_clean = lugar.upper()
    for ciudad, coords in respaldos.items():
        if ciudad in lugar_clean:
            return coords

    # 2. Si no es conocida, intentar búsqueda rápida con timeout agresivo
    geolocator = Nominatim(user_agent="vault_logic_v1")
    try:
        # Solo esperamos 3 segundos. Si no responde, saltamos al default.
        location = geolocator.geocode(lugar, timeout=3)
        if location:
            return {"lat": location.latitude, "lon": location.longitude}
    except:
        pass

    # 3. RESPALDO TOTAL: Si todo falla, devolvemos una coordenada neutra 
    # para que el sistema de vectores PUEDA CALCULAR y no dé error de enlace.
    return {"lat": 0.0, "lon": 0.0, "nota": "fallback_active"}
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
    try:
        # 1. Parsing de Fecha y Hora
        año, mes, día = map(int, fecha_str.split('-'))
        hora, minuto = map(int, hora_str.split(':'))
        
        # 2. Conversión a Julian Day
        hora_decimal = hora + (minuto / 60.0)
        jd = swe.julday(año, mes, día, hora_decimal)

        # 3. Puntos de Datos
        puntos = {
            "SOL": swe.SUN, "LUNA": swe.MOON, "MERCURIO": swe.MERCURY, 
            "VENUS": swe.VENUS, "MARTE": swe.MARS, "JUPITER": swe.JUPITER, 
            "SATURNO": swe.SATURN
        }

        vectores = {}
        for nombre, codigo in puntos.items():
            # Llamada a la librería
            resultado = swe.calc_ut(jd, codigo)
            
            # EXTRACCIÓN RADICAL:
            # Si es una tupla (o tupla de tuplas), entramos hasta encontrar el primer número
            while isinstance(resultado, (tuple, list)):
                resultado = resultado[0]
            
            # Ahora 'resultado' es garantizadamente un número (float)
            vectores[nombre] = round(float(resultado), 4)

        return vectores

    except Exception as e:
        print(f"DEBUG FINAL: {e}")
        return {"status": "error_extraccion_bruta", "detalle": str(e)}

def analizar_geometria_kepler(vectores):
    aspectos_encontrados = []
    nombres = list(vectores.keys())
    
    # Ángulos de interés (Kepler/Addey) y sus significados lógicos
    definiciones = {
        0: {"tipo": "CONJUNCIÓN", "label": "Singularidad de Energía"},
        60: {"tipo": "SEXTIL", "label": "Oportunidad Operativa"},
        90: {"tipo": "CUADRATURA", "label": "Tensión Estructural"},
        120: {"tipo": "TRÍGONO", "label": "Fluidez de Expansión"},
        180: {"tipo": "OPOSICIÓN", "label": "Punto de Contraste"}
    }
    
    orbe_maximo = 5.0 # Margen de error de 5 grados

    for i in range(len(nombres)):
        for j in range(i + 1, len(nombres)):
            p1, p2 = nombres[i], nombres[j]
            v1, v2 = vectores[p1], vectores[p2]
            
            # Calcular distancia angular mínima en un círculo
            distancia = abs(v1 - v2)
            if distancia > 180: distancia = 360 - distancia
            
            # Verificar si encaja en algún ángulo de Kepler
            for angulo_base, info in definiciones.items():
                if abs(distancia - angulo_base) <= orbe_maximo:
                    aspectos_encontrados.append({
                        "puntos": f"{p1}-{p2}",
                        "distancia": round(distancia, 2),
                        "tipo": info["tipo"],
                        "descripcion": info["label"]
                    })
    
    return aspectos_encontrados

@app.post("/consultar")
async def consultar(datos: dict):
    # 1. Limpieza de Entradas
    email = datos.get('email', '').strip().lower()
    nombre = datos.get('nombre', 'VIP MEMBER').strip().upper()
    if not nombre: nombre = "VIP MEMBER"
    lugar = datos.get('lugar', '').strip().upper()
    fecha = datos.get('fecha', '1980-01-01')
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

    # 3. Procesar Nuevo: Geolocalización y Vectores Matemáticos
    coords = obtener_gps(lugar)

    # EJECUCIÓN DEL MOTOR DE PRECISIÓN (Etapa 1)
    try:
        vectores = calcular_vectores_natales(fecha, hora, coords)
    except Exception as e:
        print(f"Error en Motor de Vectores: {e}")
        vectores = {"status": "error_calculo"}

    # --- ETAPA 2: ANALIZADOR DE ÁNGULOS (KEPLER LOGIC) ---
    geometria_hits = analizar_geometry_kepler(vectores)
    
    # Generamos la directiva dinámica basada en el primer "Hit" matemático encontrado
    if isinstance(geometria_hits, list) and len(geometria_hits) > 0:
        hit = geometria_hits[0] # Tomamos el aspecto más relevante
        directiva = f"PROTOCOLO {hit['tipo']} DETECTADO: {hit['descripcion']} entre los vectores {hit['puntos']}. Distancia: {hit['distancia']}°."
    else:
        directiva = "NODO DE EXPANSIÓN ACTIVO: Estructura geométrica en equilibrio. Momento de consolidación estratégica."

    # 4. Guardado en Supabase (Bóveda con Inteligencia Geométrica)
    try:
        supabase.table("clientes_vip").upsert({
            "email": email,
            "nombre": nombre,
            "datos_natales": {
                "lugar_original": lugar,
                "hora_nacimiento": hora,
                "fecha": fecha
            },
            "mapatotal": {
                "geo": coords, 
                "vectores_eclipticos": vectores,
                "analisis_kepler": geometria_hits, # Guardamos la lista completa de ángulos
                "directive": directiva, 
                "auth": "VERIFIED_VAULT"
            },
            "nivel_suscripcion": "free"
        }, on_conflict="email").execute()
    except Exception as e:
        print(f"Error Supabase: {e}")

    # 5. Sincronización Externa
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
