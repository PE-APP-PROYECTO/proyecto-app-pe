from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import (
    PasswordUpdateSchema,
    UserResponseSchema,
    UserUpdateSchema,
    UsuarioCreateSchema,
)
from app.services.user_service import UserService
from app.core.login import get_current_user_with_role

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

# Toda la gestión de usuarios suele ser exclusiva para Administradores
@router.post("/", response_model=UserResponseSchema, dependencies=[Depends(get_current_user_with_role(["admin"]))], status_code=status.HTTP_201_CREATED)
def crear_usuario(user: UsuarioCreateSchema, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.create(user)

@router.get("/", response_model=List[UserResponseSchema], dependencies=[Depends(get_current_user_with_role(["admin"]))])
def mostrar_usuarios(db: Session = Depends(get_db)):
    service = UserService(db)
    print(service.list())
    return service.list()

@router.get("/{user_id}", response_model=UserResponseSchema, dependencies=[Depends(get_current_user_with_role(["admin"]))])
def mostrar_por_id(user_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.get_by_id(user_id)

@router.put("/{user_id}", response_model=UserResponseSchema, dependencies=[Depends(get_current_user_with_role(["admin"]))])
def actualizar_usuario(
    user_id: int,
    datos: UserUpdateSchema,
    db: Session = Depends(get_db),
):
    service = UserService(db)
    return service.update(user_id, datos)

@router.patch("/{user_id}/cambiar-password", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_user_with_role(["admin", "empleado"]))])
def cambiar_password(
    user_id: int,
    datos: PasswordUpdateSchema,
    db: Session = Depends(get_db),
):
    service = UserService(db)
    service.change_password(user_id, datos)
    return None

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_user_with_role(["admin"]))])
def eliminar_usuario(user_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    service.delete(user_id)
    return None
