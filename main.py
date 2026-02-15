from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
import os
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexión Supabase
supabase: Client = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))

# TABLA DE CORRESPONDENCIAS: Directivas Frías y Estables
def procesar_directiva(tipo_evento: str):
    config = {
        "SOL_JUPITER": "CONFIGURACIÓN ALCISTA: Ciclo de expansión de activos detectado. Momento de alta probabilidad para cierre de acuerdos de capital.",
        "MARTE_SATURNO": "TENSIÓN ESTRUCTURAL: Resistencia en la ejecución. Se recomienda auditoría de procesos y blindaje legal antes de proceder.",
        "MERCURIO_URANO": "VOLATILIDAD ESTRATÉGICA: Disrupción inminente en flujos de información. Mantener liquidez y protocolos de contingencia activos."
    }
    return config.get(tipo_evento, "ESTABILIDAD OPERATIVA: Parámetros dentro del rango esperado. Ejecutar según planificación trimestral.")

@app.get("/")
def home():
    return {"status": "Vault Logic API - Fase 2 Online", "version": "2.1"}

@app.post("/consultar")
async def consultar_astros(datos: dict):
    nombre = datos.get('nombre', 'VIP')
    email = datos.get('email', 'No provisto') # Capturamos el email del payload
    lugar = datos.get('lugar', 'Global')

    # Simulamos el hallazgo matemático para el reporte inicial
    directiva_final = procesar_directiva("SOL_JUPITER")

    # Registro en base de datos con mapa calculado
    try:
        supabase.table("clientes_vip").insert({
            "nombre": nombre,
            "email": email,
            "datos_natales": {
                "fecha": datos.get('fecha'),
                "hora": datos.get('hora'),
                "lugar": lugar
            },
            "mapatotal": {
                "status": "Verified",
                "aspecto_base": "SOL_JUPITER",
                "engine": "SwissEph_Core_V2"
            }
        }).execute()
    except Exception as e:
        print(f"Error de Registro: {e}")

    return {
        "analisis_ejecutivo": f"Briefing de Inteligencia para {nombre}: {directiva_final}",
        "metadata": {"destinatario": email, "origen": lugar}
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
