# Módulo de Inteligencia Artificial - Tienda de Celulares 🤖📱

Microservicio REST construido con **FastAPI**, **LangChain** y **Google Gemini (gemini-3.6-flash)** que analiza datos de productos en tiempo real provistos por el Backend para responder preguntas en lenguaje natural.

---

## 🚀 Requisitos e Instalación

1. **Crear y activar entorno virtual (opcional pero recomendado):**
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Linux/Mac:
   source venv/bin/activate
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar variables de entorno:**
   Crea un archivo `.env` basado en `.env.example`:
   ```env
   GOOGLE_API_KEY=tu-api-key-de-gemini-aqui
   ```

---

## 🏃‍♂️ Ejecución

Para iniciar el servidor localmente en el puerto `8080`:

```bash
python chatbot_gemini.py
```

- **Servidor:** `http://localhost:8080`
- **Documentación Interactiva (Swagger):** `http://localhost:8080/docs`

---

## 📡 Endpoints

### 1. Health Check
- **Método:** `GET /`
- **Descripción:** Verifica que el microservicio está activo.

### 2. Chat / Consulta Inteligente
- **Método:** `POST /chat`
- **Headers:** `Content-Type: application/json`

#### Payload de entrada (`Request Body`):
```json
{
  "pregunta": "¿Cuál es el celular Samsung más económico disponible?",
  "listado_productos": [
    {
      "id": 1,
      "nombre": "Galaxy S24",
      "marca": "Samsung",
      "precio": 899,
      "stock": 10,
      "color": "Negro"
    },
    {
      "id": 2,
      "nombre": "Galaxy A54",
      "marca": "Samsung",
      "precio": 450,
      "stock": 25,
      "color": "Azul"
    }
  ]
}
```

#### Respuesta (`Response Body`):
```json
{
  "respuesta": "El celular Samsung más económico en el catálogo actual es el Galaxy A54 con un precio de $450 y contamos con 25 unidades en stock.",
  "status": "ok"
}
```
