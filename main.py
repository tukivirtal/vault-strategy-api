from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
import os
import uvicorn

app = FastAPI()

# Configuración de seguridad (CORS) 
# Corregido: ["*"] permite que Vercel pueda enviar los datos al servidor
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
    return {"status": "SaaS Ejecutivo Activo", "version": "1.3"}

@app.post("/consultar")
async def consultar_astros(datos: dict):
    # 1. Extraemos los datos del formulario de Vercel
    nombre = datos.get('nombre', 'Usuario Anónimo')
    fecha = datos.get('fecha')
    hora = datos.get('hora')
    lugar = datos.get('lugar')

    # 2. Lógica de Guardado en Supabase
    try:
        # Preparamos el objeto JSON para la columna datos_natales
        datos_natales = {
            "fecha": fecha,
            "hora": hora,
            "lugar": lugar
        }
        
        # Enviamos SOLO las columnas que no dan error (nombre y datos_natales)
        # Nota: Omitimos 'email' porque no lo estamos pidiendo en el diseño aún
        supabase.table("clientes_vip").insert({
            "nombre": nombre,
            "datos_natales": datos_natales
        }).execute()
        
    except Exception as e:
        # Si falla, verás el error detallado en los Logs de Render
        print(f"Error guardando en Supabase: {str(e)}")

    # 3. Respuesta de Estrategia para el diseño dorado
    return {
        "analisis_ejecutivo": f"Análisis de Bóveda para {nombre}: La frecuencia planetaria sobre {lugar} para el ciclo {fecha} indica una ventana de ejecución estratégica optimizada. Se recomienda acción directa desde las {hora}."
    }

# Corrección vital del ejecutable
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
