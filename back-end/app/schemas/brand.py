from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

# --- CREACIÓN ---
class CreateBrandSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Nombre de la marca")
    description: Optional[str] = Field(None, max_length=100, description="Descripción opcional")

# --- ACTUALIZACION DE MARCAS ---
class UpdateBrandSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50, description="Nombre de la marca")
    description: Optional[str] = Field(None, max_length=100, description="Descripción de la marca")

# --- RESPUESTA DE CONSULTA ---
class BrandResponseSchema(BaseModel):
    id: int  
    name: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)