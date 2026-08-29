"""Lógica de negocio para las marcas."""

from typing import List, Optional

from sqlalchemy import select

from app.models import Brand, Product
from app.services.base_service import BaseService
from app.utils import ConflictError, NotFoundError
from app.schemas.brand import CreateBrandSchema, UpdateBrandSchema


class BrandService(BaseService):
    """Servicio para gestionar marcas con sus reglas de negocio."""

    model = Brand
    not_found_message = "Marca no encontrada"

    def create(self, schema: CreateBrandSchema) -> Brand:
        """Crea una marca nueva validando datos y unicidad del nombre.

        Args:
            data: Diccionario con los datos de la marca (name y description).

        Returns:
            La marca creada en la base de datos.
        """
        self._ensure_unique_name(schema.name)
        return super().create(schema.model_dump())

    def update(self, brand_id: int, schema: UpdateBrandSchema) -> Brand:
        """Actualiza una marca de forma parcial.

        Args:
            brand_id: Identificador de la marca a actualizar.
            data: Diccionario con los campos que se van a modificar.

        Returns:
            La marca con los cambios aplicados.
        """
        update_data = schema.model_dump(exclude_unset=True)

        if "name" in update_data:
            self._ensure_unique_name(update_data["name"], exclude_id=brand_id)

        return super().update(brand_id, update_data)

    def list(self) -> List[Brand]:
        """Obtiene el listado de marcas usando la sesión de BD inyectada en BaseService."""
        query = select(Brand)
        return self.db.scalars(query).all()

    def get_by_id(self, brand_id:int)-> Brand:
      """Obtiene una marca por su ID o lanza NotFoundError si no existe."""
      query = select(Brand).where(Brand.id == brand_id)
      brand = self.db.scalar(query)
      if not brand:
        raise NotFoundError(f"Marca con ID {brand_id} no encontrada")
      return brand

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

    def delete_logico(self, brand_id: int) -> Brand:
      brand = self.get_by_id(brand_id)

      if self._has_active_products(brand_id):
        raise ConflictError(
          "No se puede desactivar la marca por que tiene productos activos asociados"
        )
      brand.is_active = False
      self.db.commit()
      self.db.refresh(brand)
      return brand

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
