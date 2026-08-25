from fastapi import APIRouter
from app.routes import (
    login,
    marcas,
    productos,
    proveedores,
    usuarios
)

router = APIRouter()

router.include_router(usuarios.router)
router.include_router(login.router)
router.include_router(marcas.router)
router.include_router(productos.router)
router.include_router(proveedores.router)
