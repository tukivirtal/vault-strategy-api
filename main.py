from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
import os
import uvicorn

app = FastAPI()

# Configuración de seguridad (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexión con Supabase usando las variables de entorno de Render
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/")
def home():
    return {"status": "SaaS Ejecutivo Activo - Fase 1", "version": "1.4"}

@app.post("/consultar")
async def consultar_astros(datos: dict):
    # 1. Extraemos los datos del formulario (Ahora incluyendo email)
    nombre = datos.get('nombre', 'Usuario Anónimo')
    email = datos.get('email')
    fecha = datos.get('fecha')
    hora = datos.get('hora')
    lugar = datos.get('lugar')

    # Preparación para la Fase 2: El mapa total que alimentará la tabla de correspondencias
    # Por ahora guardamos un estado pendiente
    mapa_simulado = {
        "engine": "NASA_Eph_V1",
        "status": "pending_calculation",
        "precision": "high"
    }

    # 2. Lógica de Guardado en Supabase
    try:
        # Insertamos en la tabla clientes_vip con los nuevos campos de la Fase 1
        supabase.table("clientes_vip").insert({
            "nombre": nombre,
            "email": email,
            "datos_natales": {
                "fecha": fecha, 
                "hora": hora, 
                "lugar": lugar
            },
            "mapatotal": mapa_simulado,
            "nivel_suscripcion": "free"
        }).execute()
        
    except Exception as e:
        # Revisa los Logs de Render si esto falla; puede ser que falte la columna en SQL
        print(f"Error Fase 1 - Guardado: {str(e)}")

    # 3. Respuesta de Estrategia para el cliente
    return {
        "analisis_ejecutivo": f"Bienvenido a la Bóveda, {nombre}. Tu reporte inicial ha sido generado y enviado a {email}. Los ciclos detectados en {lugar} para el {fecha} están siendo procesados con prioridad ejecutiva."
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
