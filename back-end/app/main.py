import logging
from datetime import datetime, timezone, timedelta
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from app.config import settings
from app.core.exception_handlers import register_exception_handlers
from app.database import Base, engine
from app.routes.index import router as api_router

import app.models  # noqa: F401

# UTC-5 Colombia
COLOMBIA_TZ = timezone(timedelta(hours=-5))

# Formateador personalizado para forzar la hora de Colombia en los logs
class ColombiaFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, tz=COLOMBIA_TZ)
        if datefmt:
            return dt.strftime(datefmt)
        return dt.isoformat()

# Configurar el logger principal y el de Uvicorn
log_format = "[%(asctime)s] [%(levelname)s] - %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

formatter = ColombiaFormatter(log_format, datefmt=date_format)

# Aplica el formato a la consola
handler = logging.StreamHandler()
handler.setFormatter(formatter)

# Configura los loggers de la app y de uvicorn.access
for logger_name in ("tecApp", "uvicorn", "uvicorn.access"):
    l = logging.getLogger(logger_name)
    l.handlers = [handler]
    l.setLevel(logging.INFO)

app = FastAPI(title="tecApp Backend")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    fecha_hora = datetime.now(COLOMBIA_TZ).strftime("%Y-%m-%d %H:%M:%S")

    logging.getLogger("tecApp").error(
        f"[{fecha_hora}] Excepción no controlada en {request.method} {request.url.path}\n"
        f"Detalle del error: {str(exc)}",
        exc_info=True
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "timestamp": fecha_hora,
            "path": request.url.path,
            "message": "Error interno del servidor",
            "detail": str(exc)
        }
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
