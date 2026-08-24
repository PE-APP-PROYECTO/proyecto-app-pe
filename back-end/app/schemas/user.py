from typing import Optional
from pydantic import BaseModel, Field, EmailStr, model_validator, ConfigDict


# --- CREACIÓN ---
class UsuarioCreateSchema(BaseModel):
    fullName: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    document: str = Field(..., min_length=6, max_length=11)
    password: str = Field(..., min_length=8, max_length=50)
    confirm_password: str = Field(..., min_length=8, max_length=50)

    # Valida que las contraseñas sean idénticas
    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Las contraseñas no coinciden")
        return self


# --- ACTUALIZACIÓN DE PERFIL ---
class UserUpdateSchema(BaseModel):
    fullName: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    document: Optional[str] = Field(None, min_length=6, max_length=11)
    is_active: Optional[bool] = None


# --- CAMBIO DE CONTRASEÑA ---
class PasswordUpdateSchema(BaseModel):  # Se renombró con P mayúscula (Buena práctica)
    current_password: str = Field(..., min_length=8, max_length=50)
    new_password: str = Field(..., min_length=8, max_length=50)
    confirm_new_password: str = Field(..., min_length=8, max_length=50)

    # Valida que la nueva contraseña coincida con la confirmación
    @model_validator(mode="after")
    def check_new_passwords_match(self):
        if self.new_password != self.confirm_new_password:
            raise ValueError("La nueva contraseña y su confirmación no coinciden")
        if self.current_password == self.new_password:
            raise ValueError("La nueva contraseña no puede ser igual a la actual")
        return self

# ---  RESPUESTA DE CONSULTA ---
class UserResponseSchema(BaseModel):
    id: int
    fullName: str
    email: EmailStr
    document: str

    model_config = ConfigDict(from_attributes=True)
