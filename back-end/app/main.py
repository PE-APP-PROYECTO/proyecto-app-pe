from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

import json
import os

from app.database import Base, engine, SessionLocal
import app.models  # noqa: F401 - necesario para registrar los modelos en Base.metadata

app = FastAPI(title="tecApp Backend")

Base.metadata.create_all(bind=engine)

# Configurar CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajusta esto con la URL de tu frontend en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("cargando backend tecApp...")

@app.get("/")
def read_root():
    return {"message": "¡Backend de tecApp funcionando correctamente!"}
