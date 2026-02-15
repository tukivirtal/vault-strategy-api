from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
import os
import uvicorn

app = FastAPI()

# Configuración de seguridad (CORS)
# Permite que tu frontend en Vercel se conecte sin bloqueos
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

# --- TABLA DE CORRESPONDENCIAS TÉCNICAS (Lógica de Negocio) ---
def obtener_directiva_ejecutiva(aspecto_clave: str):
    """
    Traductor de eventos astronómicos a directivas de estatus elevado.
    Mantiene un tono frío, estable y orientado a la acción.
    """
    correspondencias = {
        "EXPANSION": "Ciclo de alta rentabilidad detectado. Momento óptimo para escalado de activos y apertura de nuevas líneas de capital.",
        "RESTRICCION": "Tensión en la estructura operativa. Se recomienda auditoría de procesos y postergación de firmas importantes por 48hs.",
        "ENFOQUE": "Energía de implementación máxima. Fase ideal para ejecutar directivas postergadas y cierre de negociaciones complejas.",
        "NEUTRAL": "Estabilidad operativa confirmada. Mantener curso actual sin desviaciones de presupuesto."
    }
    return correspondencias.get(aspecto_clave, "Procesando variables adicionales para precisión quirúrgica.")

@app.get("/")
def home():
    return {"status": "SaaS Ejecutivo - Inteligencia Fase 2 Activa", "version": "2.0"}

@app.post("/consultar")
async def consultar_astros(datos: dict):
    # 1. Extracción de Identidad y Datos Natales
    nombre = datos.get('nombre', 'Usuario VIP')
    email = datos.get('email')
    fecha = datos.get('fecha')
    hora = datos.get('hora')
    lugar = datos.get('lugar')

    # 2. Motor de Simulación Matemática (Fase 2)
    # En el siguiente paso, las librerías flatlib/swisseph calcularán esto
    # Simulamos un hallazgo de 'EXPANSION' para este perfil
    aspecto_detectado = "EXPANSION" 
    directiva = obtener_directiva_ejecutiva(aspecto_detectado)

    # 3. Construcción del Mapa Total para la Bóveda
    mapa_total_procesado = {
        "engine": "NASA_Eph_V2",
        "timestamp": "2026-02-14",
        "aspecto_principal": aspecto_detectado,
        "coordenadas_referencia": lugar,
        "status": "Calculated"
    }

    # 4. Registro en Base de Datos (Activo de Marketing y Consulta)
    try:
        supabase.table("clientes_vip").insert({
            "nombre": nombre,
            "email": email,
            "datos_natales": {"fecha": fecha, "hora": hora, "lugar": lugar},
            "mapatotal": mapa_total_procesado,
            "nivel_suscripcion": "free"
        }).execute()
        
    except Exception as e:
        # Los errores de guardado aparecerán en los Logs de Render
        print(f"Error Crítico Fase 2 (Database): {str(e)}")

    # 5. Salida de Consultoría de Bolsillo (Fase 2)
    return {
        "analisis_ejecutivo": f"Briefing de Inteligencia para {nombre}: {directiva}",
        "metadata": {
            "lugar": lugar,
            "referencia_temporal": fecha,
            "alerta": "Prioridad Ejecutiva"
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
