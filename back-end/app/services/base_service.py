"""Servicio base con operaciones CRUD compartidas."""

from typing import Any, Dict, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.services.exceptions import NotFoundError


class BaseService:
    """Clase base de los servicios.

    Aporta el CRUD genérico para que cada servicio concreto
    solo tenga que agregar sus reglas de negocio.
    """

    model: Any = None
    not_found_message = "Recurso no encontrado"
    PROTECTED_FIELDS = {"id", "created_at", "updated_at"}

    def __init__(self, db: Session):
        self.db = db

    def list(self, skip: int = 0, limit: int = 100, only_active: bool = True) -> List[Any]:
        """Devuelve una lista paginada de registros."""
        query = select(self.model)

        if only_active and hasattr(self.model, "is_active"):
            query = query.where(self.model.is_active.is_(True))

        query = query.offset(skip).limit(limit)
        return list(self.db.scalars(query).all())

    def get_by_id(self, resource_id: int) -> Any:
        """Devuelve un registro por su id o lanza NotFoundError."""
        obj = self.db.get(self.model, resource_id)

        if obj is None:
            raise NotFoundError(self.not_found_message)

        return obj

    def create(self, data: Dict[str, Any]) -> Any:
        """Crea un registro nuevo a partir de un diccionario de datos."""
        obj = self.model(**data)

        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)

        return obj

    def update(self, resource_id: int, data: Dict[str, Any]) -> Any:
        """Actualiza un registro existente; ignora campos protegidos."""
        obj = self.get_by_id(resource_id)

        for key, value in data.items():
            if key in self.PROTECTED_FIELDS:
                continue
            if hasattr(obj, key):
                setattr(obj, key, value)

        self.db.commit()
        self.db.refresh(obj)

        return obj

    def delete(self, resource_id: int) -> Any:
        """Desactiva el registro (borrado lógico).

        Si el modelo no tuviera is_active, hace borrado físico.
        """
        obj = self.get_by_id(resource_id)

        if hasattr(obj, "is_active"):
            obj.is_active = False
        else:
            self.db.delete(obj)

        self.db.commit()

        return obj