import logging
from datetime import datetime
from zoneinfo import ZoneInfo
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
# Importa tus excepciones personalizadas
from app.utils.exceptions import (
    NotFoundError,
    UnauthorizedError,
    ValidationError,
)
COLOMBIA_TZ = ZoneInfo("America/Bogota")
logger = logging.getLogger("tecApp")

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

   # Dentro de tu función de registro:
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        fecha_hora_co = datetime.now(COLOMBIA_TZ).strftime("%Y-%m-%d %H:%M:%S")
        logger.warning(f"[{fecha_hora_co}] HTTP {exc.status_code} en {request.method} {request.url.path}: {exc.detail}")

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "timestamp": fecha_hora_co,
                "timezone": "America/Bogota (UTC-5)",
                "path": request.url.path,
                "detail": exc.detail
            }
        )
