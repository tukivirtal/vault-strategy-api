from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from geopy.geocoders import Nominatim
import os
import uvicorn
import httpx  # Para disparar el envío de mail vía API

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
RESEND_API_KEY = os.environ.get("RESEND_API_KEY") # Nueva: Configúrala en Render

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- PLANTILLA DE CORREO PROFESIONAL (Guardada en una variable) ---
HTML_EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html>
<body style="margin: 0; padding: 0; background-color: #000; font-family: Arial, sans-serif; color: #fff;">
    <div style="max-width: 600px; margin: 0 auto; border: 1px solid #1a1a1a; background-color: #0a0a0a; padding: 40px;">
        <h1 style="color: #d4af37; letter-spacing: 5px; text-align: center;">VAULT LOGIC</h1>
        <p style="text-transform: uppercase; font-size: 12px; color: #888; text-align: center;">Briefing de Inteligencia Inicial</p>
        <hr style="border: 0; border-top: 1px solid #1a1a1a; margin: 20px 0;">
        <p>Estimado/a <strong>{nombre}</strong>,</p>
        <p>El motor de efemérides ha procesado sus coordenadas natales. Se ha generado una directiva estratégica:</p>
        <div style="border-left: 3px solid #d4af37; padding-left: 20px; margin: 30px 0; font-size: 18px;">
            {directiva}
        </div>
        <p style="font-family: monospace; font-size: 11px; color: #555;">
            GEO-REF: {lat}, {lon}<br>
            STATUS: NIVEL_FREE_LIMITADO
        </p>
        <div style="text-align: center; margin-top: 40px;">
            <a href="https://tu-sitio.vercel.app/vip" style="background-color: #d4af37; color: #000; padding: 15px 25px; text-decoration: none; font-weight: bold; font-size: 12px; display: inline-block;">ELEVAR A ESTATUS VIP</a>
        </div>
    </div>
</body>
</html>
"""

def obtener_gps(lugar):
    try:
        geolocator = Nominatim(user_agent="vault_logic_pro")
        location = geolocator.geocode(lugar)
        if location:
            return {"lat": round(location.latitude, 4), "lon": round(location.longitude, 4)}
    except:
        pass
    return {"lat": -34.4, "lon": -58.5} # Default por si falla la API

async def enviar_email(email_destino, nombre, directiva, coords):
    """Función para enviar el correo usando la API de Resend"""
    if not RESEND_API_KEY:
        print("Aviso: No se detectó RESEND_API_KEY. Correo no enviado.")
        return

    url = "https://api.resend.com/emails"
    headers = {"Authorization": f"Bearer {RESEND_API_KEY}", "Content-Type": "application/json"}
    
    payload = {
        "from": "Vault Logic <onboarding@resend.dev>", # Cambia esto cuando valides tu dominio
        "to": [email_destino],
        "subject": f"DIRECTIVA ESTRATÉGICA: {nombre}",
        "html": HTML_EMAIL_TEMPLATE.format(
            nombre=nombre, 
            directiva=directiva, 
            lat=coords['lat'], 
            lon=coords['lon']
        )
    }

    async with httpx.AsyncClient() as client:
        await client.post(url, headers=headers, json=payload)

@app.post("/consultar")
async def consultar(datos: dict):
    # Estandarización de Datos
    nombre = datos.get('nombre', 'USUARIO').upper()
    email = datos.get('email', '').lower()
    lugar = datos.get('lugar', '').upper()
    
    # 1. Localización Real
    coords = obtener_gps(lugar)
    
    # 2. Lógica de Inteligencia
    directiva = "VENTANA DE ESCALABILIDAD ALTA: Sincronía detectada en ciclos de crecimiento. Momento óptimo para la inyección de capital."

    # 3. Guardado Inteligente (UPSERT) en Supabase
    # Si el email existe, actualiza. Si no, crea registro.
    try:
        supabase.table("clientes_vip").upsert({
            "email": email,
            "nombre": nombre,
            "datos_natales": datos,
            "mapatotal": {"geo": coords, "status": "VERIFIED"},
            "nivel_suscripcion": "free"
        }, on_conflict="email").execute()
    except Exception as e:
        print(f"Error Database: {e}")

    # 4. Disparo de Correo Electrónico
    await enviar_email(email, nombre, directiva, coords)

    # 5. Respuesta a la Web
    return {
        "titulo": "DIRECTIVA ESTRATÉGICA GENERADA",
        "analisis_ejecutivo": directiva,
        "coordinadas": f"LAT: {coords['lat']} | LON: {coords['lon']}",
        "firma": "VAULT LOGIC SYSTEM"
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
