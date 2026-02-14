from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
import os
import uvicorn

app = FastAPI()

# Configuración de seguridad (CORS) para que Vercel pueda hablar con Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción cambiaremos esto por tu URL de Vercel
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexión con Supabase usando las variables de entorno que pegaste en Render
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/")
def home():
    return {"status": "SaaS Ejecutivo Activo", "version": "1.1"}

@app.post("/consultar")
async def consultar_astros(datos: dict):
    # 1. Extraemos los datos que vienen del index.html
    nombre = datos.get('nombre', 'Usuario Anónimo')
    fecha = datos.get('fecha')
    hora = datos.get('hora')
    lugar = datos.get('lugar')

    # 2. Lógica de Guardado en Supabase (clientes_vip)
    try:
        # Combinamos los datos en un JSON para la columna datos_natales
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
        print(f"Error guardando en Supabase: {e}")
        # Seguimos adelante aunque falle el guardado para no romper la experiencia del usuario

    # 3. Respuesta de Estrategia (Aquí es donde integraremos la librería astronómica después)
    return {
        "analisis_ejecutivo": f"Análisis para {nombre}: El cielo sobre {lugar} muestra una configuración estratégica sólida para la fecha {fecha}. Los ciclos indican una ventana de ejecución óptima entre las {hora} y el cierre de jornada."
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
