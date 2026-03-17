from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Esto evita el error de "Sincronización" en el navegador
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_index():
    # Sirve el panel directamente desde la raíz
    return FileResponse('genesis-live.html')

@app.get("/api/stats")
async def get_stats():
    # Datos temporales para que el panel se vea "VIVO" 
    # mientras arreglamos la conexión real
    return {
        "capital": 24.8,
        "negociacion": 12.2,
        "riesgo": -18.5,
        "status": "ACTIVE"
    }
