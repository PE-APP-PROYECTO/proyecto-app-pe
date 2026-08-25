from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.config import settings
from app.core.exception_handlers import register_exception_handlers
from app.database import Base, engine
from app.routes.index import router as api_router

import app.models  # noqa: F401 - necesario para registrar los modelos en Base.metadata

print("cargando backend tecApp...")

app = FastAPI(title="tecApp Backend")

# Configurar CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajusta esto con la URL de tu frontend en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

register_exception_handlers(app)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "¡Backend de tecApp funcionando correctamente!"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=settings.APP_PORT, reload=True)

