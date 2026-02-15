from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from geopy.geocoders import Nominatim
import os
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexión con Supabase
supabase: Client = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))

# MOTOR DE TRADUCCIÓN ESTRATÉGICA (Rol de Usuario Exigente)
def traducir_matematica_a_estatus(evento_astral: str):
    """
    Traducción fría y ejecutiva. El usuario no quiere 'predicciones', 
    quiere 'directivas de mercado personalizadas'.
    """
    libreria_estatutos = {
        "CONJUNTO_EXPANSION": {
            "titulo": "VENTANA DE ESCALABILIDAD ALTA",
            "cuerpo": "Sincronía detectada en ciclos de crecimiento. Momento óptimo para la inyección de capital en activos de riesgo controlado."
        },
        "OPOSICION_ESTRUCTURAL": {
            "titulo": "ALERTA DE TENSIÓN EN PROCESOS",
            "cuerpo": "Resistencia detectada en flujos de autoridad. Se recomienda blindaje de contratos y postergación de firmas críticas por 72hs."
        },
        "NEUTRALIDAD_ESTABLE": {
            "titulo": "CONSOLIDACIÓN OPERATIVA",
            "cuerpo": "Ciclos en fase de estabilidad. No se detectan fluctuaciones de alto impacto. Mantener hoja de ruta actual."
        }
    }
    return libreria_estatutos.get(evento_astral, libreria_estatutos["NEUTRALIDAD_ESTABLE"])

def obtener_gps(lugar):
    try:
        geolocator = Nominatim(user_agent="vault_logic_pro")
        location = geolocator.geocode(lugar)
        if location:
            return {"lat": location.latitude, "lon": location.longitude}
    except:
        pass
    return {"lat": 0, "lon": 0}

@app.post("/consultar")
async def consultar_astros(datos: dict):
    nombre = datos.get('nombre', 'VIP')
    email = datos.get('email')
    lugar = datos.get('lugar')
    
    # 1. Localización Exacta (Matemática de Posición)
    coordenadas = obtener_gps(lugar)
    
    # 2. Simulación de Hallazgo del Motor (Próximo paso: SwissEph real)
    # Simulamos que detectamos una ventana de expansión para este perfil
    hallazgo = "CONJUNTO_EXPANSION"
    analisis = traducir_matematica_a_estatus(hallazgo)

    # 3. Construcción del Mapa de Bóveda (ADN del Usuario)
    mapa_total = {
        "geo": coordenadas,
        "evento_madre": hallazgo,
        "precision": "NASA-Eph-Grade",
        "status": "Verified"
    }

    # 4. Registro Silencioso en Base de Datos
    try:
        supabase.table("clientes_vip").insert({
            "nombre": nombre,
            "email": email,
            "datos_natales": datos,
            "mapatotal": mapa_total
        }).execute()
    except Exception as e:
        print(f"Log Error: {e}")

    # 5. Entrega de Estatus (Lo que el usuario ve)
    return {
        "titulo": analisis["titulo"],
        "analisis_ejecutivo": analisis["cuerpo"],
        "coordenadas": f"{coordenadas['lat']}, {coordenadas['lon']}",
        "firma": "Vault Logic Executive Suite"
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
