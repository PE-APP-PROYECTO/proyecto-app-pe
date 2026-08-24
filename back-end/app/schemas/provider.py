from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict

# --- CREACIÓN ---
class CreateProviderSchema(BaseModel):
    company_name: str = Field(..., min_length=5, max_length=100, description="Razón social del proveedor")
    
    # Solo permite números o guiones (ej. 12345678-9)
    nit: str = Field(..., pattern=r"^[0-9\-]{8,12}$", description="NIT o número de identificación fiscal")
    
    # Solo permite números y opcionalmente el signo + al inicio
    phone: str = Field(..., pattern=r"^\+?[0-9]{8,13}$", description="Número de teléfono de contacto")
    
    email: EmailStr
    address: str = Field(..., min_length=1, max_length=100, description="Dirección de la empresa")

# --- ACTUALIZACION DE PROVEEDORES ---
class UpdateProviderSchema(BaseModel):
    company_name: Optional[str] = Field(None, min_length=5, max_length=100)
    nit: Optional[str] = Field(None, pattern=r"^[0-9\-]{8,12}$")
    phone: Optional[str] = Field(None, pattern=r"^\+?[0-9]{8,13}$")
    email: Optional[EmailStr] = None
    address: Optional[str] = Field(None, min_length=1, max_length=100)

# --- RESPUESTA DE CONSULTA ---
class ProviderResponseSchema(BaseModel):
    id: int
    company_name: str
    nit: str
    phone: Optional[str] = None
    email: EmailStr
    address: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
