"""Servicio base con operaciones CRUD compartidas.

Define el comportamiento común de todos los servicios del módulo
(listar con paginación, obtener por id, crear, actualizar y eliminar)
para que cada servicio concreto solo agregue sus reglas de negocio.
"""

from typing import Any, Dict, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.utils import NotFoundError


class BaseService:
    """Clase base de los servicios.

    Aporta el CRUD genérico sobre el modelo de SQLAlchemy que cada
    subclase define en su atributo ``model``.
    """

    model: Any = None
    not_found_message = "Recurso no encontrado"
    PROTECTED_FIELDS = {"id", "created_at", "updated_at"}

    def __init__(self, db: Session):
        """Inicializa el servicio con una sesión activa de base de datos.

        Args:
            db: Sesión de SQLAlchemy usada para todas las operaciones.
        """
        self.db = db

    def list(self, skip: int = 0, limit: int = 100, only_active: bool = True) -> List[Any]:
        """Devuelve una lista paginada de registros.

        Args:
            skip: Cantidad de registros a omitir antes de devolver resultados.
            limit: Cantidad máxima de registros a devolver.
            only_active: Si es True y el modelo tiene ``is_active``,
                solo se devuelven registros activos.

        Returns:
            Lista de registros encontrados.
        """
        query = select(self.model)

        if only_active and hasattr(self.model, "is_active"):
            query = query.where(self.model.is_active.is_(True))

        query = query.offset(skip).limit(limit)
        return list(self.db.scalars(query).all())

    def get_by_id(self, resource_id: int) -> Any:
        """Devuelve un registro a partir de su identificador.

        Args:
            resource_id: Identificador del registro buscado.

        Returns:
            El registro encontrado.

        Raises:
            NotFoundError: Si no existe ningún registro con ese identificador.
        """
        obj = self.db.get(self.model, resource_id)

        if obj is None:
            raise NotFoundError(self.not_found_message)

        return obj

    def create(self, data: Dict[str, Any]) -> Any:
        """Crea un registro nuevo a partir de un diccionario de datos.

        Args:
            data: Diccionario con los campos y valores del registro.

        Returns:
            El registro creado en la base de datos.
        """
        obj = self.model(**data)

        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)

        return obj

    def update(self, resource_id: int, data: Dict[str, Any]) -> Any:
        """Actualiza de forma parcial un registro existente.

        Ignora los campos protegidos (id, created_at, updated_at) y
        cualquier clave que no exista en el modelo.

        Args:
            resource_id: Identificador del registro a actualizar.
            data: Diccionario con los campos que se van a modificar.

        Returns:
            El registro con los cambios aplicados.

        Raises:
            NotFoundError: Si no existe ningún registro con ese identificador.
        """
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
        """Elimina un registro usando borrado lógico cuando es posible.

        Si el modelo tiene el campo ``is_active`` el registro se
        desactiva; de lo contrario se hace borrado físico.

        Args:
            resource_id: Identificador del registro a eliminar.

        Returns:
            El registro eliminado o desactivado.

        Raises:
            NotFoundError: Si no existe ningún registro con ese identificador.
        """
        obj = self.get_by_id(resource_id)

        if hasattr(obj, "is_active"):
            obj.is_active = False
        else:
            self.db.delete(obj)

        self.db.commit()

        return obj