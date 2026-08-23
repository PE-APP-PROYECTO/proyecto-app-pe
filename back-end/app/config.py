import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DB_URL: str = (
        "postgresql+psycopg2://"
        + os.getenv("DB_USER_SECRET")
        + ":"
        + os.getenv("DB_PASSWORD_SECRET")
        + "@"
        + os.getenv("DB_HOST")
        + ":"
        + os.getenv("DB_PORT")
        + "/"
        + os.getenv("DB_NAME")
    )
    JWT_SECRET: str = os.getenv("JWT_SECRET", "supersecreto")
    JWT_ALGORITHM: str = "HS256"
    # Credenciales de acceso desde el .env
    ADMIN_USER: str = os.getenv("ADMIN_USER", "admin")
    ADMIN_PASSWORD_HASH: str = os.getenv("ADMIN_PASSWORD_HASH", "")


settings = Settings()
