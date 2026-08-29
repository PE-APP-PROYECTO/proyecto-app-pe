from typing import List, Optional
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.product import ProductResponseSchema, CreateProductSchema, UpdateProductSchema, ChatProductRequestSchema, ChatProductResponseSchema
from app.services.product_service import ProductService
from app.core.login import get_current_user_with_role

router = APIRouter(prefix="/productos", tags=["Productos"])

# RUTA PÚBLICA: Consultar productos con IA (chatbot)
@router.post("/chat", response_model=ChatProductResponseSchema)
@router.post("/chat/", response_model=ChatProductResponseSchema, include_in_schema=False)
def chat_con_ia(payload: ChatProductRequestSchema, db: Session = Depends(get_db)):
    """Envía la pregunta y el listado de productos a la API externa de IA."""
    service = ProductService(db)
    result = service.chat_with_ai(payload.question)
    return result

# RUTA PÚBLICA: Cualquier usuario puede listar productos sin Token
@router.get("/", response_model=List[ProductResponseSchema])
def list_products(
    skip: int = Query(0, ge=0, description="Registros a omitir para paginación"),
    limit: int = Query(100, ge=1, le=500, description="Límite máximo de resultados"),
    only_active: bool = Query(True, description="Filtrar solo productos activos"),
    search: Optional[str] = Query(None, description="Buscar por referencia, descripción o color"),
    brand_id: Optional[int] = Query(None, description="Filtrar por ID de marca"),
    provider_id: Optional[int] = Query(None, description="Filtrar por ID de proveedor"),
    db: Session = Depends(get_db),
):
    """Obtiene el listado público de productos."""
    service = ProductService(db)
    return service.list(
        skip=skip,
        limit=limit,
        only_active=only_active,
        search=search,
        brand_id=brand_id,
        provider_id=provider_id,
    )

# RUTA PÚBLICA: Ver detalle de un producto
@router.get("/{product_id}", response_model=ProductResponseSchema)
def obtener_producto_por_id(product_id: int, db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.get_by_id(product_id)

# RUTAS PROTEGIDAS (Solo Admin)
@router.post("/", response_model=ProductResponseSchema, dependencies=[Depends(get_current_user_with_role(["admin"]))], status_code=status.HTTP_201_CREATED)
def crear_producto(producto: CreateProductSchema, db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.create(producto)

@router.put("/{product_id}", response_model=ProductResponseSchema, dependencies=[Depends(get_current_user_with_role(["admin"]))])
def actualizar_producto(product_id: int, producto: UpdateProductSchema, db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.update(product_id, producto)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_user_with_role(["admin"]))])
def eliminar_producto(product_id: int, db: Session = Depends(get_db)):
    service = ProductService(db)
    service.delete(product_id)
    return None
