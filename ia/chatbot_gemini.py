import os
import json
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
import uvicorn

# =====================================================================
# Rutas seguras (para que funcione desde cualquier terminal)
# =====================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# =====================================================================
# Carga la API Key desde el archivo .env (nunca se sube a GitHub)
# =====================================================================
load_dotenv(os.path.join(BASE_DIR, ".env"))

if not os.environ.get("GOOGLE_API_KEY"):
    print("❌ ERROR: No se encontró la variable GOOGLE_API_KEY.")
    print("   Crea un archivo .env con: GOOGLE_API_KEY=tu-clave-aqui")
    print("   (Mira .env.example como referencia)")
    exit(1)

# =====================================================================
# Inicialización de la API
# =====================================================================
app = FastAPI(
    title="API Chatbot Tienda de Celulares",
    description="Chatbot de IA que analiza datos de productos en tiempo real enviados por el Backend usando Google Gemini.",
    version="2.0.0"
)

# CORS: Permite que el Frontend / Backend hagan peticiones desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================================
# Inicialización del motor de IA
# =====================================================================
print("[*] Iniciando el motor de Gemini...")
llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash")
print("[OK] Motor de IA listo.")

# =====================================================================
# Modelos de datos para la API
# =====================================================================
class PreguntaRequest(BaseModel):
    pregunta: str
    listado_productos: Optional[List[Dict[str, Any]]] = None

class RespuestaResponse(BaseModel):
    respuesta: str
    status: str

# =====================================================================
# Endpoints
# =====================================================================

@app.get("/")
def health_check():
    """Verifica que el servidor está activo."""
    return {
        "mensaje": "API del Chatbot de Tienda de Celulares está activa.",
        "status": "ok",
        "version": "2.0.0",
        "uso": "Envía un POST a /chat con JSON: {\"pregunta\": \"...\", \"listado_productos\": [{...}]}"
    }

@app.post("/chat", response_model=RespuestaResponse)
def chat(req: PreguntaRequest):
    """
    Recibe una pregunta en lenguaje natural y opcionalmente el listado de productos
    directamente desde el Backend, devolviendo la respuesta analizada por Gemini.
    """
    try:
        # Formatear el listado de productos si se envió en la petición
        if req.listado_productos:
            datos_json = json.dumps(req.listado_productos, ensure_ascii=False, indent=2)
            contexto_productos = f"""
LISTADO DE PRODUCTOS EN TIEMPO REAL (Enviado por Backend):
{datos_json}
"""
        else:
            contexto_productos = """
(No se adjuntó lista de productos en esta petición. Responde amablemente de forma general o indica que no hay productos cargados actualmente).
"""

        instruccion_sistema = f"""Eres el asistente experto de una tienda de celulares.
Tu objetivo es responder a las consultas analizando los datos de los productos que te son provistos en tiempo real.

{contexto_productos}

Instrucciones:
1. Responde de forma clara, concisa y en español.
2. Utiliza los datos provistos en el listado para responder sobre precios, características, stock, marcas o comparaciones.
3. Si el usuario pregunta por un producto que no está en la lista, indícaselo cortésmente.
4. No inventes información que no esté presente en los datos.
"""

        # Estructura del mensaje para LangChain
        historial = [
            SystemMessage(content=instruccion_sistema),
            HumanMessage(content=req.pregunta)
        ]
        
        # Invocación a Gemini
        respuesta = llm.invoke(historial)
        
        # Extracción del texto
        texto = respuesta.content
        if isinstance(texto, list):
            texto = next(
                (item['text'] for item in texto if item.get('type') == 'text'),
                str(texto)
            )
        
        return RespuestaResponse(respuesta=texto, status="ok")
        
    except Exception as e:
        return RespuestaResponse(
            respuesta=f"Error al procesar la pregunta: {str(e)}",
            status="error"
        )

# =====================================================================
# Arranque del servidor
# =====================================================================
if __name__ == "__main__":
    print("\n" + "="*55)
    print(" CHATBOT DE TIENDA DE CELULARES - API REST (v2.0 Dinámica)")
    print("="*55)
    print(" Servidor corriendo en: http://localhost:8080")
    print(" Documentacion interactiva: http://localhost:8080/docs")
    print("="*55 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8080)
