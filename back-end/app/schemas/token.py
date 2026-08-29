from pydantic import BaseModel,Field

# Schema para la SALIDA (Respuesta)
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str |None = None
    role: str | None = None

# Schema para la ENTRADA (Payload de la petición)
class LoginRequest(BaseModel):
    username: str = Field(..., description="Nombre de usuario")
    password: str = Field(..., description="Contraseña")