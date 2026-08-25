from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.provider import (
    CreateProviderSchema,
    ProviderResponseSchema,
    UpdateProviderSchema,
)
from app.services.provider_service import ProviderService
from app.core.login import get_current_user_with_role

router = APIRouter(prefix="/proveedores", tags=["Proveedores"])

@router.post("/", response_model=ProviderResponseSchema, dependencies=[Depends(get_current_user_with_role(["admin"]))], status_code=status.HTTP_201_CREATED)
def crear_proveedor(provider: CreateProviderSchema, db: Session = Depends(get_db)):
    service = ProviderService(db)
    return service.create(provider)

@router.get("/", response_model=List[ProviderResponseSchema], dependencies=[Depends(get_current_user_with_role(["admin", "empleado"]))])
def mostrar_proveedores(db: Session = Depends(get_db)):
    service = ProviderService(db)
    return service.list()

@router.get("/{provider_id}", response_model=ProviderResponseSchema, dependencies=[Depends(get_current_user_with_role(["admin", "empleado"]))])
def mostrar_por_id(provider_id: int, db: Session = Depends(get_db)):
    service = ProviderService(db)
    return service.get_by_id(provider_id)

@router.put("/{provider_id}", response_model=ProviderResponseSchema, dependencies=[Depends(get_current_user_with_role(["admin"]))])
def actualizar_proveedor(
    provider_id: int,
    datos: UpdateProviderSchema,
    db: Session = Depends(get_db),
):
    service = ProviderService(db)
    return service.update(provider_id, datos)

@router.delete("/{provider_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_user_with_role(["admin"]))])
def eliminar_proveedor(provider_id: int, db: Session = Depends(get_db)):
    service = ProviderService(db)
    service.delete(provider_id)
    return None
