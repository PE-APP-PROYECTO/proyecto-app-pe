"""Lógica de negocio para las marcas."""

from typing import Any, Dict, Optional

from sqlalchemy import select

from app.models import Brand, Product
from app.services.base_service import BaseService
from app.services.exceptions import ConflictError
from app.services.validators import validate_max_length, validate_required


class BrandService(BaseService):
    """Servicio para gestionar marcas con sus reglas de negocio."""

    model = Brand
    not_found_message = "Marca no encontrada"

    def create(self, data: Dict[str, Any]) -> Brand:
        """Crea una marca nueva validando datos y unicidad del nombre.

        Args:
            data: Diccionario con los datos de la marca (name y description).

        Returns:
            La marca creada en la base de datos.
        """
        self._validate_data(data)
        self._ensure_unique_name(data["name"])
        return super().create(data)

    def update(self, brand_id: int, data: Dict[str, Any]) -> Brand:
        """Actualiza una marca de forma parcial.

        Args:
            brand_id: Identificador de la marca a actualizar.
            data: Diccionario con los campos que se van a modificar.

        Returns:
            La marca con los cambios aplicados.
        """
        if "name" in data:
            validate_required(data["name"], "name")
            validate_max_length(data["name"], 100, "name")
            self._ensure_unique_name(data["name"], exclude_id=brand_id)

        if "description" in data:
            validate_required(data["description"], "description")
            validate_max_length(data["description"], 255, "description")

        return super().update(brand_id, data)

    def delete(self, brand_id: int) -> Brand:
        """Desactiva la marca si no tiene productos activos asociados.

        Args:
            brand_id: Identificador de la marca a desactivar.

        Returns:
            La marca desactivada.
        """
        if self._has_active_products(brand_id):
            raise ConflictError(
                "No se puede desactivar la marca porque tiene productos activos asociados."
            )
        return super().delete(brand_id)

    def _validate_data(self, data: Dict[str, Any]) -> None:
        """Valida campos obligatorios y longitudes máximas de la marca."""
        validate_required(data.get("name"), "name")
        validate_required(data.get("description"), "description")
        validate_max_length(data.get("name"), 100, "name")
        validate_max_length(data.get("description"), 255, "description")

    def _ensure_unique_name(self, name: str, exclude_id: Optional[int] = None) -> None:
        """Lanza ConflictError si ya existe otra marca con el mismo nombre."""
        query = select(Brand.id).where(Brand.name == name)

        if exclude_id is not None:
            query = query.where(Brand.id != exclude_id)

        if self.db.scalar(query) is not None:
            raise ConflictError(f"Ya existe una marca con el nombre '{name}'.")

    def _has_active_products(self, brand_id: int) -> bool:
        """Devuelve True si la marca tiene productos activos asociados."""
        query = select(Product.id).where(
            Product.brand_id == brand_id,
            Product.is_active.is_(True),
        )
        return self.db.scalar(query) is not None