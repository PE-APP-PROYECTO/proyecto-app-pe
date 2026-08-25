from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.services.brand_service import BrandService
from app.schemas.brand import BrandResponseSchema, CreateBrandSchema, UpdateBrandSchema
from app.database import get_db
from app.core.login import get_current_user_with_role

router = APIRouter(prefix="/marcas", tags=["Marcas"])

# RUTA PÚBLICA: Obtener marcas
@router.get("/", response_model=list[BrandResponseSchema])
def listar_marcas(db: Session = Depends(get_db)):
    service = BrandService(db)
    return service.list()

# RUTA PÚBLICA: Obtener marca por ID
@router.get("/{brand_id}", response_model=BrandResponseSchema)
def mostrar_por_id(brand_id: int, db: Session = Depends(get_db)):
    service = BrandService(db)
    return service.get_by_id(brand_id)

# RUTAS PROTEGIDAS (Solo Admin)
@router.post("/", response_model=BrandResponseSchema, dependencies=[Depends(get_current_user_with_role(["admin"]))], status_code=status.HTTP_201_CREATED)
def crear_marca(schema: CreateBrandSchema, db: Session = Depends(get_db)):
    service = BrandService(db)
    return service.create(schema)

@router.patch("/{brand_id}", response_model=BrandResponseSchema, dependencies=[Depends(get_current_user_with_role(["admin"]))])
def actualizar_marca(brand_id: int, schema: UpdateBrandSchema, db: Session = Depends(get_db)):
    service = BrandService(db)
    return service.update(brand_id, schema)

@router.delete("/{brand_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_user_with_role(["admin"]))])
def eliminar_marca(brand_id: int, db: Session = Depends(get_db)):
    service = BrandService(db)
    service.delete(brand_id)
    return None

@router.delete("/inactivate/{brand_id}", response_model=BrandResponseSchema, dependencies=[Depends(get_current_user_with_role(["admin"]))])
def inactivate_brand(brand_id: int, db: Session = Depends(get_db)):
    service = BrandService(db)
    return service.delete_logico(brand_id)
