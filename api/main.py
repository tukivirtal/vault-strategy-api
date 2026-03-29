from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import json
import math
import random
import urllib.request
from datetime import datetime
from supabase import create_client, Client
import uvicorn

app = FastAPI()

# 1. SEGURIDAD (CORS) - Puertas abiertas para Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# 2. CONEXIÓN A LA BASE DE DATOS
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 3. ESTRUCTURAS DE DATOS
class LoginData(BaseModel):
    email: str
    password: str
    login_only: bool = False
    nombre: str = None
    lugar: str = None
    fecha: str = None
    hora: str = None
    lat: str = None
    lon: str = None

class PerfilRequest(BaseModel):
    email: str

class SimulacionRequest(BaseModel):
    email: str
    fecha_inicio: str
    fecha_fin: str

class UpgradeRequest(BaseModel):
    email: str
    nivel_suscripcion: str

class SoporteRequest(BaseModel):
    email_usuario: str
    plan_nivel: str
    mensaje: str
    estado: str = "ABIERTO"

# 4. RUTAS DEL SISTEMA

@app.post("/upgrade_nivel")
async def upgrade_nivel(req: UpgradeRequest):
    if not supabase:
        return {"status": "error", "mensaje": "Base de datos desconectada"}
    try:
        response = supabase.table("clientes_vip").update({"nivel_suscripcion": req.nivel_suscripcion}).eq("email", req.email).execute()
        return {"status": "success", "mensaje": f"Nivel actualizado a {req.nivel_suscripcion}"}
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}

@app.post("/consultar")
async def consultar(data: LoginData):
    if not supabase:
        return {"status": "error", "analisis_ejecutivo": "Error interno: Base de datos no conectada."}
        
    try:
        response = supabase.table("clientes_vip").select("*").eq("email", data.email).execute()
        user = response.data[0] if response.data else None

        if data.login_only:
            if not user:
                return {"status": "error", "analisis_ejecutivo": "El correo no existe en nuestros registros."}
            if str(user.get("password")) != str(data.password):
                return {"status": "error", "analisis_ejecutivo": "Contraseña estratégica incorrecta."}
            return {"status": "success"}
        else:
            if user:
                if str(user.get("password")) != str(data.password):
                    return {"status": "error", "analisis_ejecutivo": "El correo ya está registrado con otra contraseña."}
                return {"status": "exists"}
            
            nuevo_usuario = {
                "email": data.email,
                "password": data.password,
                "nombre": data.nombre,
                "datos_natales": json.dumps({
                    "fecha": data.fecha,
                    "hora": data.hora,
                    "lugar_original": data.lugar,
                    "lat": data.lat,
                    "lon": data.lon
                }),
                "nivel_suscripcion": "FREE"
            }
            supabase.table("clientes_vip").insert(nuevo_usuario).execute()
            return {"status": "success"}
            
    except Exception as e:
        return {"status": "error", "analisis_ejecutivo": f"Fallo en la base de datos: {str(e)}"}

@app.post("/obtener_perfil")
async def obtener_perfil(req: PerfilRequest):
    if not supabase:
        return {"status": "error"}
    try:
        response = supabase.table("clientes_vip").select("*").eq("email", req.email).execute()
        if response.data:
            return {"status": "success", "datos": response.data[0]}
        return {"status": "error"}
    except Exception as e:
        return {"status": "error"}

@app.post("/simular_periodo")
async def simular_periodo(req: SimulacionRequest):
    if not supabase:
        return {"status": "error", "mensaje": "Núcleo de base de datos desconectado"}

    try:
        response = supabase.table("clientes_vip").select("*").eq("email", req.email).execute()
        if not response.data:
            return {"status": "error", "mensaje": "Sujeto no identificado"}

        user = response.data[0]
        vectores = {}
        mapatotal_str = user.get("mapatotal")
        
        if mapatotal_str:
            mapa_obj = json.loads(mapatotal_str) if isinstance(mapatotal_str, str) else mapatotal_str
            if "vectores_eclipticos" in mapa_obj:
                vectores = mapa_obj["vectores_eclipticos"]

        if not vectores:
            seed = sum(ord(c) for c in req.email)
            vectores = { "SOL": (seed % 360), "LUNA": ((seed * 2) % 360), "JUPITER": ((seed * 7) % 360), "SATURNO": ((seed * 11) % 360) }

        f_inicio = datetime.strptime(req.fecha_inicio, "%Y-%m-%d")
        f_fin = datetime.strptime(req.fecha_fin, "%Y-%m-%d")
        dias_desde_2000 = (f_inicio - datetime(2000, 1, 1)).days
        dias_totales = max(1, (f_fin - f_inicio).days)

        jupiter_natal = vectores.get("JUPITER", 0)
        saturno_natal = vectores.get("SATURNO", 0)
        sol_natal = vectores.get("SOL", 0)
        luna_natal = vectores.get("LUNA", 0)

        ciclo_jupiter = math.sin(math.radians(((dias_desde_2000 % 4332) / 4332 * 360) - jupiter_natal))
        ciclo_saturno = math.cos(math.radians(((dias_desde_2000 % 10759) / 10759 * 360) - saturno_natal))
        ciclo_sol = math.sin(math.radians(((dias_desde_2000 % 365) / 365 * 360) - sol_natal))

        val_cap = round((ciclo_jupiter * 18) + (ciclo_sol * 10), 1)
        val_neg = round((ciclo_sol * 12) - (ciclo_saturno * 8), 1)
        val_risk = round((ciclo_saturno * -20) + (ciclo_jupiter * -5), 1)

        is_risk = val_risk < -5 or val_cap < 0

        curva_exacta = []
        for i in range(7):
            dia_segmento = dias_desde_2000 + int((dias_totales / 6) * i)
            c_jup = math.sin(math.radians(((dia_segmento % 4332) / 4332 * 360) - jupiter_natal))
            c_sat = math.cos(math.radians(((dia_segmento % 10759) / 10759 * 360) - saturno_natal))
            c_sol = math.sin(math.radians(((dia_segmento % 365) / 365 * 360) - sol_natal))
            c_luna = math.sin(math.radians(((dia_segmento % 28) / 28 * 360) - luna_natal)) 
            
            if is_risk:
                punto = int(50 + (c_sat * 25) - (c_jup * 10) + (c_sol * 10) + (c_luna * 15)) 
            else:
                punto = int(50 + (c_jup * 25) - (c_sat * 10) + (c_sol * 10) + (c_luna * 15))
                
            punto = max(5, min(100, punto))
            curva_exacta.append(punto)

        if is_risk:
            estado, estrategia, modo = "RIESGO ESTRUCTURAL", "Posición Defensiva", "DEFENSA"
            directiva = "Los vectores matemáticos indican alta fricción en este ciclo. <b>Acción:</b> Congele contrataciones y eleve liquidez."
        else:
            estado, estrategia, modo = "SINCRONÍA ÓPTIMA", "Inversión Agresiva", "EXPANSIÓN"
            directiva = "Ventana de resonancia expansiva confirmada. <b>Acción:</b> Acelere cierres de ventas y expanda presupuestos de marketing."

        return {
            "status": "success",
            "datos": {
                "cap": f"{'+' if val_cap > 0 else ''}{val_cap}%",
                "neg": f"{'+' if val_neg > 0 else ''}{val_neg}%",
                "risk": f"{'+' if val_risk > 0 else ''}{val_risk}%",
                "estado": estado,
                "estrategia": estrategia,
                "directiva": directiva,
                "modo": modo,
                "curva_exacta": curva_exacta,
                "rango": f"{req.fecha_inicio} A {req.fecha_fin}"
            }
        }
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}

@app.get("/api/health")
def health():
    return {"status": "online", "system": "VAULT LOGIC ACTIVE"}

# ==========================================
# MÓDULO DE SOPORTE TÁCTICO Y MAILERLITE
# ==========================================
@app.post("/generar_ticket")
async def generar_ticket(req: SoporteRequest):
    if not supabase:
        return {"status": "error", "mensaje": "Base de datos desconectada"}
    
    try:
        # 1. Generamos el código exacto de su sistema
        codigo = str(random.randint(10000, 99999))
        ticket_ref = f"GX-{codigo}"
        
        # 2. Guardamos en la tabla 'soporte_tickets' de Supabase
        nuevo_ticket = {
            "ticket_ref": ticket_ref,
            "email_usuario": req.email_usuario,
            "plan_nivel": req.plan_nivel,
            "mensaje": req.mensaje
        }
        supabase.table("soporte_tickets").insert(nuevo_ticket).execute()
        print(f"✅ Ticket {ticket_ref} guardado en Bóveda.")
        
        # 3. CONEXIÓN DIRECTA CON MAILERLITE
        ml_api_key = os.getenv("MAILERLITE_API_KEY")
        ml_group_id = os.getenv("MAILERLITE_GROUP_ID")
        
        if ml_api_key and ml_group_id:
            url = "https://connect.mailerlite.com/api/subscribers"
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {ml_api_key}"
            }
            data = {
                "email": req.email_usuario,
                "groups": [ml_group_id]
            }
            req_ml = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')
            try:
                urllib.request.urlopen(req_ml)
                print(f"✉️ Señal enviada a MailerLite para {req.email_usuario}")
            except Exception as ml_err:
                print("❌ Error contactando a MailerLite:", ml_err)

        return {"status": "success", "ticket_id": ticket_ref, "mensaje": "Ticket indexado exitosamente."}
        
    except Exception as e:
        print("❌ Error en Ticket:", str(e))
        return {"status": "error", "mensaje": "Fallo en el núcleo de soporte."}

# ==========================================
# RUTA OFICIAL DE PAYPAL
# ==========================================
@app.post("/webhook/paypal")
async def paypal_webhook(request: Request):
    try:
        payload = await request.json()
        event_type = payload.get("event_type")
        print(f"📡 SEÑAL DE PAYPAL RECIBIDA: {event_type}")

        if event_type in ["PAYMENT.CAPTURE.COMPLETED", "CHECKOUT.ORDER.APPROVED"]:
            resource = payload.get("resource", {})
            custom_id = resource.get("custom_id")
            monto = resource.get("amount", {}).get("value") 
            
            if custom_id and supabase:
                nivel = "EXECUTIVE" if float(monto) > 20 else "SENTINEL"
                supabase.table("clientes_vip").update({"nivel_suscripcion": nivel}).eq("email", custom_id).execute()
                print(f"✅ Base de datos verificada para: {custom_id} -> Nivel: {nivel}")

        return {"status": "success", "mensaje": "Transmisión de PayPal recibida"}
        
    except Exception as e:
        print("❌ Error procesando Webhook de PayPal:", str(e))
        return {"status": "error", "mensaje": "Señal con errores internos"}

# ==========================================
# EL MOTOR DE ARRANQUE PARA RENDER
# ==========================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
