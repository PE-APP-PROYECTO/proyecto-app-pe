from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

# --- CREACIÓN ---
class CreateProductSchema(BaseModel):
    reference: str = Field(..., min_length=3, max_length=30, description="Referencia única del producto")
    price: int = Field(..., ge=0, description="Precio en enteros, debe ser positivo")
    color: str = Field(..., min_length=2, max_length=20)
    brand_id: int = Field(..., gt=0, description="ID de marca válido (> 0)")
    stock: int = Field(..., ge=0, description="Cantidad disponible en inventario")
    description: Optional[str] = Field(None, max_length=100)  
    provider_id: int = Field(..., gt=0, description="ID de proveedor válido (> 0)")

# --- ACTUALIZACIÓN DE PRODUCTOS ---
class UpdateProductSchema(BaseModel):
    reference: Optional[str] = Field(None, min_length=3, max_length=30)
    price: Optional[int] = Field(None, ge=0)
    color: Optional[str] = Field(None, min_length=2, max_length=20)
    brand_id: Optional[int] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    description: Optional[str] = Field(None, max_length=100)
    provider_id: Optional[int] = Field(None, gt=0)

# --- RESPUESTA DE CONSULTA ---
class ProductResponseSchema(BaseModel):
    id: int
    reference: str
    price: int
    color: str
    brand_id: int
    stock: int
    description: Optional[str] = None  
    provider_id: int

    model_config = ConfigDict(from_attributes=True)

# --- CHAT CON IA SOBRE PRODUCTOS ---
class ChatProductRequestSchema(BaseModel):
    question: str = Field(..., min_length=1, description="Pregunta del usuario sobre los productos")

class ChatProductResponseSchema(BaseModel):
    answer: str = Field(..., description="Respuesta generada por la IA")
    status: str = Field(..., description="Estado de la respuesta de la API")