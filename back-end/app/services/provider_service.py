"""Lógica de negocio para los proveedores."""

from typing import List, Optional
from sqlalchemy import select

from app.models import Product, Provider
from app.schemas.provider import CreateProviderSchema, UpdateProviderSchema
from app.services.base_service import BaseService
from app.utils import ConflictError


class ProviderService(BaseService):
    """Servicio para gestionar proveedores con sus reglas de negocio."""

    model = Provider
    not_found_message = "Proveedor no encontrado"

    def create(self, schema: CreateProviderSchema) -> Provider:
        """Crea un proveedor nuevo validando campos únicos."""
        self._ensure_unique_value(
            Provider.nit,
            schema.nit,
            f"Ya existe un proveedor con el NIT '{schema.nit}'.",
        )
        self._ensure_unique_value(
            Provider.email,
            schema.email,
            f"Ya existe un proveedor con el correo '{schema.email}'.",
        )
        return super().create(schema.model_dump())

    def update(self, provider_id: int, schema: UpdateProviderSchema) -> Provider:
        """Actualiza un proveedor de forma parcial."""
        update_data = schema.model_dump(exclude_unset=True)

        if not update_data:
            return self.get_by_id(provider_id)

        if "nit" in update_data:
            self._ensure_unique_value(
                Provider.nit,
                update_data["nit"],
                f"Ya existe un proveedor con el NIT '{update_data['nit']}'.",
                exclude_id=provider_id,
            )

        if "email" in update_data:
            self._ensure_unique_value(
                Provider.email,
                update_data["email"],
                f"Ya existe un proveedor con el correo '{update_data['email']}'.",
                exclude_id=provider_id,
            )

        return super().update(provider_id, update_data)

    def list(self) -> List[Provider]:
        """Devuelve el listado completo de proveedores."""
        query = select(Provider)
        return self.db.scalars(query).all()

    def delete(self, provider_id: int) -> Provider:
        """Desactiva o elimina el proveedor si no tiene productos activos asociados."""
        if self._has_active_products(provider_id):
            raise ConflictError(
                "No se puede desactivar el proveedor porque tiene productos activos asociados."
            )
        return super().delete(provider_id)

    # ------------------------------------------------------------------
    # Helpers internos
    # ------------------------------------------------------------------

    def _has_active_products(self, provider_id: int) -> bool:
        """Devuelve True si el proveedor tiene productos activos asociados."""
        query = select(Product.id).where(
            Product.provider_id == provider_id,
            Product.is_active.is_(True),
        )
        return self.db.scalar(query) is not None

    def _ensure_unique_value(
        self,
        column,
        value: str,
        error_message: str,
        exclude_id: Optional[int] = None,
    ) -> None:
        """Lanza ConflictError si otro registro ya usa ese valor único."""
        query = select(Provider.id).where(column == value)

        if exclude_id is not None:
            query = query.where(Provider.id != exclude_id)

        if self.db.scalar(query) is not None:
            raise ConflictError(error_message)
