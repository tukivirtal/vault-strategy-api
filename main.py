from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from geopy.geocoders import Nominatim
from pydantic import BaseModel, EmailStr
from typing import Optional
import os
import uvicorn
import httpx
import swisseph as swe

app = FastAPI()

# --- CONFIGURACIÓN DE CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CREDENCIALES ---
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- MODELO DE DATOS (PYDANTIC) ---
# Este es el "recepcionista" que valida que los datos traigan password
class UserData(BaseModel):
    nombre: Optional[str] = None
    email: str
    password: str  # Campo obligatorio ahora
    fecha: Optional[str] = None
    hora: Optional[str] = None
    lugar: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    login_only: Optional[bool] = False

# --- MOTOR DE CÁLCULO ---
def calcular_vectores_natales(fecha_str, hora_str, coords):
    try:
        año, mes, día = map(int, fecha_str.split('-'))
        hora, minuto = map(int, hora_str.split(':'))
        hora_decimal = hora + (minuto / 60.0)
        jd = swe.julday(año, mes, día, hora_decimal)

        puntos = {
            "SOL": swe.SUN, "LUNA": swe.MOON, "MERCURIO": swe.MERCURY, 
            "VENUS": swe.VENUS, "MARTE": swe.MARS, "JUPITER": swe.JUPITER, 
            "SATURNO": swe.SATURN
        }

        vectores = {}
        for nombre, codigo in puntos.items():
            resultado = swe.calc_ut(jd, codigo)
            while isinstance(resultado, (tuple, list)):
                resultado = resultado[0]
            vectores[nombre] = round(float(resultado), 4)
        return vectores
    except Exception as e:
        return {"error": str(e)}

def analizar_geometria_kepler(vectores):
    aspectos = []
    nombres = list(vectores.keys())
    definiciones = {
        0: {"tipo": "CONJUNCIÓN", "label": "Singularidad"},
        60: {"tipo": "SEXTIL", "label": "Oportunidad"},
        90: {"tipo": "CUADRATURA", "label": "Tensión"},
        120: {"tipo": "TRÍGONO", "label": "Fluidez"},
        180: {"tipo": "OPOSICIÓN", "label": "Contraste"}
    }
    for i in range(len(nombres)):
        for j in range(i + 1, len(nombres)):
            p1, p2 = nombres[i], nombres[j]
            v1, v2 = vectores[p1], vectores[p2]
            dist = abs(v1 - v2)
            if dist > 180: dist = 360 - dist
            for ang, info in definiciones.items():
                if abs(dist - ang) <= 5.0:
                    aspectos.append({"puntos": f"{p1}-{p2}", "tipo": info["tipo"], "descripcion": info["label"]})
    return aspectos

# --- ENDPOINT PRINCIPAL: CONSULTAR / REGISTRAR ---
@app.post("/consultar")
async def consultar(user: UserData):
    email_clean = user.email.strip().lower()
    
    # 1. Verificar si el usuario ya existe en Supabase
    check = supabase.table("clientes_vip").select("*").eq("email", email_clean).execute()
    
    if check.data:
        # LÓGICA DE LOGIN (ACCESO VIP)
        db_user = check.data[0]
        # Verificamos si la contraseña coincide
        if db_user.get("password") == user.password:
            return {
                "status": "exists",
                "titulo": "ACCESO AUTORIZADO",
                "analisis_ejecutivo": f"Bienvenido de nuevo, {db_user['nombre']}. Terminal vinculada.",
                "email": email_clean
            }
        else:
            return {
                "status": "error",
                "analisis_ejecutivo": "CREDENTIAL_ERROR: Contraseña incorrecta para esta terminal."
            }

    # 2. Si no existe y es login_only, error
    if user.login_only:
        return {
            "status": "error",
            "analisis_ejecutivo": "USER_NOT_FOUND: Este email no tiene una terminal registrada."
        }

    # 3. PROCESO DE REGISTRO NUEVO
    lat = user.lat if user.lat is not None else -33.9968
    lon = user.lon if user.lon is not None else -58.2836
    coords = {"lat": lat, "lon": lon}

    vectores = calcular_vectores_natales(user.fecha, user.hora, coords)
    geometria = analizar_geometria_kepler(vectores)
    
    directiva = f"PROTOCOLO {geometria[0]['tipo']} ACTIVO" if geometria else "ESTABILIDAD ARMÓNICA"

    payload_db = {
        "email": email_clean,
        "nombre": user.nombre.upper() if user.nombre else "VIP MEMBER",
        "password": user.password, # Guardamos la clave
        "datos_natales": {"lugar_original": user.lugar, "hora_nacimiento": user.hora, "fecha": user.fecha},
        "mapatotal": {
            "geo": coords,
            "vectores_eclipticos": vectores,
            "analisis_kepler": geometria,
            "directive": directiva,
            "auth": "VERIFIED_VAULT"
        }
    }

    try:
        supabase.table("clientes_vip").insert(payload_db).execute()
        return {
            "status": "success",
            "analisis_ejecutivo": "TERMINAL VINCULADA CON ÉXITO.",
            "email": email_clean
        }
    except Exception as e:
        return {"status": "error", "analisis_ejecutivo": f"DB_ERROR: {str(e)}"}

# --- ENDPOINT PARA LA BÓVEDA ---
@app.get("/obtener_reporte/{email}")
async def obtener_reporte(email: str):
    try:
        res = supabase.table("clientes_vip").select("*").eq("email", email.strip().lower()).execute()
        if not res.data:
            return {"status": "error", "message": "Firma no detectada."}
        
        user = res.data[0]
        return {
            "status": "success",
            "data": {
                "nombre": user['nombre'],
                "directiva": user['mapatotal']['directive'],
                "mapatotal": user['mapatotal'], # Aquí enviamos los vectores para el radar
                "geo_ref": f"LAT: {user['mapatotal']['geo']['lat']}"
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
