from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Esto permite que tu página web (Vercel) se comunique con tu servidor (Railway)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "SaaS Ejecutivo Activo", "version": "1.0"}

@app.post("/consultar")
def consultar_astros(datos_usuario: dict):
    # Aquí es donde el 'Cerebro' procesará los datos de la carta
    # Por ahora, devolvemos una respuesta de éxito profesional
    return {
        "analisis_ejecutivo": "Tendencia alcista para negociaciones. Ventana de poder detectada.",
        "recomendacion": "Ejecutar contratos antes del cierre de jornada."
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
