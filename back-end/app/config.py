import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DB_URL: str = (
        "postgresql+psycopg2://"
        + (os.getenv("DB_USER_SECRET") or "")
        + ":"
        + (os.getenv("DB_PASSWORD_SECRET") or "")
        + "@"
        + (os.getenv("DB_HOST") or "")
        + ":"
        + (os.getenv("DB_PORT") or "")
        + "/"
        + (os.getenv("DB_NAME") or "")
    )
    JWT_SECRET: str = os.getenv("JWT_SECRET", "supersecreto")
    JWT_ALGORITHM: str = "HS256"
    # Credenciales de acceso desde el .env
    ADMIN_USER: str = os.getenv("ADMIN_USER", "admin")

    # .strip("'\"") elimina comillas simples/dobles que vengan del .env
    ADMIN_PASSWORD_HASH: str = os.getenv("ADMIN_PASSWORD_HASH", "").strip("'\"")

    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))

    # API externa de IA (chatbot de productos)
    AI_API_URL: str = os.getenv("AI_API_URL", "https://9nd3t0wm-8080.use.devtunnels.ms")


settings = Settings()
