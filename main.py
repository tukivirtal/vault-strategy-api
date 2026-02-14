from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
import os
import uvicorn

app = FastAPI()

# Configuración de seguridad (CORS) 
# Importante: "*" permite que tu diseño en Vercel envíe datos sin bloqueos
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
    return {"status": "SaaS Ejecutivo Activo", "version": "1.2"}

@app.post("/consultar")
async def consultar_astros(datos: dict):
    # 1. Extraemos los datos que vienen del index.html
    nombre = datos.get('nombre', 'Usuario Anónimo')
    fecha = datos.get('fecha')
    hora = datos.get('hora')
    lugar = datos.get('lugar')

    # 2. Lógica de Guardado en Supabase (clientes_vip)
    try:
        # Estructura de datos para la columna JSONB de Supabase
        datos_natales = {
            "fecha": fecha,
            "hora": hora,
            "lugar": lugar
        }
        
        supabase.table("clientes_vip").insert({
            "nombre": nombre,
            "datos_natales": datos_natales,
            "nivel_suscripcion": "free"
        }).execute()
        
    except Exception as e:
        # Esto saldrá en los "Logs" de Render si algo falla
        print(f"Error guardando en Supabase: {e}")

    # 3. Respuesta de Estrategia Personalizada
    return {
        "analisis_ejecutivo": f"Análisis de Bóveda para {nombre}: La frecuencia planetaria sobre {lugar} para el ciclo {fecha} indica una ventana de ejecución estratégica optimizada. Se recomienda acción directa desde las {hora}."
    }

# Corrección del ejecutable principal
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
