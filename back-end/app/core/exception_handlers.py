# app/core/exception_handlers.py
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

# Importa tus excepciones personalizadas
from app.utils.exceptions import (
    NotFoundError,
    UnauthorizedError,
    ValidationError,
)

def register_exception_handlers(app: FastAPI) -> None:
    """Centraliza e inscribe todos los Exception Handlers en la aplicación FastAPI."""

    @app.exception_handler(UnauthorizedError)
    async def unauthorized_handler(request: Request, exc: UnauthorizedError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": str(exc)},
        )

    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)},
        )

    @app.exception_handler(ValidationError)
    async def validation_handler(request: Request, exc: ValidationError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc)},
        )
