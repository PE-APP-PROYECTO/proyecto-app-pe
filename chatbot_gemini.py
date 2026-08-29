import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
import uvicorn

# =====================================================================
# Carga la API Key desde el archivo .env (nunca se sube a GitHub)
# =====================================================================
load_dotenv()

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
    description="Chatbot de IA que analiza datos de ventas y productos de una tienda de celulares usando Google Gemini.",
    version="1.0.0"
)

# CORS: Permite que el Frontend (u otros equipos) hagan peticiones desde el navegador
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Permite cualquier origen
    allow_credentials=True,
    allow_methods=["*"],       # Permite GET, POST, etc.
    allow_headers=["*"],       # Permite cualquier header
)

# =====================================================================
# Carga de datos y modelo de IA (se ejecuta 1 sola vez al arrancar)
# =====================================================================
print("[*] Cargando bases de datos a la memoria de la IA...")
try:
    with open("productos.csv", "r", encoding="utf-8") as f:
        csv_productos = f.read()
    with open("ventas.csv", "r", encoding="utf-8") as f:
        csv_ventas = f.read()
    with open("marcas.csv", "r", encoding="utf-8") as f:
        csv_marcas = f.read()
    print("[OK] Datos cargados exitosamente.")
except FileNotFoundError as e:
    print(f"[ERROR] No se encontro el archivo {e.filename}")
    print("   Asegúrate de que los archivos CSV estén en la misma carpeta.")
    exit(1)

print("[*] Iniciando el motor de Gemini...")
llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0)

# Instrucción base con todos los datos de la tienda en memoria
instruccion_sistema = f"""
Eres el asistente experto de una tienda de celulares.
Tu memoria contiene la base de datos completa de la tienda en formato CSV (Productos, Marcas y 10,000 registros de Ventas).
Tu objetivo es responder a las preguntas del usuario analizando estos datos mentalmente y dando una respuesta clara en español.
Intenta que las respuestas sean cortas y concisas en una sola iteración.

DATOS DE PRODUCTOS:
{csv_productos}

DATOS DE MARCAS:
{csv_marcas}

HISTORIAL DE VENTAS:
{csv_ventas}
"""

print("[OK] Motor de IA listo.")

# =====================================================================
# Modelos de datos para la API (lo que recibe y lo que devuelve)
# =====================================================================
class PreguntaRequest(BaseModel):
    pregunta: str

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
        "mensaje": "API del Chatbot de Tienda de Celulares esta activa.",
        "status": "ok",
        "uso": "Envía un POST a /chat con JSON: {\"pregunta\": \"tu pregunta aquí\"}"
    }

@app.post("/chat", response_model=RespuestaResponse)
def chat(req: PreguntaRequest):
    """
    Recibe una pregunta en lenguaje natural y devuelve la respuesta
    del chatbot basada en los datos de la tienda.
    """
    try:
        # Creamos un historial fresco por cada petición (sin estado entre usuarios)
        historial = [
            SystemMessage(content=instruccion_sistema),
            HumanMessage(content=req.pregunta)
        ]
        
        # 1 sola petición a Gemini
        respuesta = llm.invoke(historial)
        
        # Extraemos el texto limpio
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
    print(" CHATBOT DE TIENDA DE CELULARES - API REST")
    print("="*55)
    print(" Servidor corriendo en: http://localhost:8080")
    print(" Documentacion interactiva: http://localhost:8080/docs")
    print("="*55 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8080)
