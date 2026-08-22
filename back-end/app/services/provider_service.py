"""Lógica de negocio para los proveedores."""

from typing import Any, Dict, Optional

from sqlalchemy import select

from app.models import Product, Provider
from app.services.base_service import BaseService
from app.services.exceptions import ConflictError
from app.services.validators import (
    validate_email,
    validate_max_length,
    validate_required,
)


class ProviderService(BaseService):
    """Servicio para gestionar proveedores con sus reglas de negocio."""

    model = Provider
    not_found_message = "Proveedor no encontrado"

    def create(self, data: Dict[str, Any]) -> Provider:
        """Crea un proveedor nuevo validando datos y campos únicos.

        Args:
            data: Diccionario con los datos del proveedor.

        Returns:
            El proveedor creado en la base de datos.
        """
        self._validate_data(data)
        self._ensure_unique_value(
            Provider.nit,
            data["nit"],
            f"Ya existe un proveedor con el NIT '{data['nit']}'.",
        )
        self._ensure_unique_value(
            Provider.email,
            data["email"],
            f"Ya existe un proveedor con el correo '{data['email']}'.",
        )
        return super().create(data)

    def update(self, provider_id: int, data: Dict[str, Any]) -> Provider:
        """Actualiza un proveedor de forma parcial.

        Args:
            provider_id: Identificador del proveedor a actualizar.
            data: Diccionario con los campos que se van a modificar.

        Returns:
            El proveedor con los cambios aplicados.
        """
        if "company_name" in data:
            validate_required(data["company_name"], "company_name")
            validate_max_length(data["company_name"], 150, "company_name")

        if "nit" in data:
            validate_required(data["nit"], "nit")
            validate_max_length(data["nit"], 20, "nit")
            self._ensure_unique_value(
                Provider.nit,
                data["nit"],
                f"Ya existe un proveedor con el NIT '{data['nit']}'.",
                exclude_id=provider_id,
            )

        if "phone" in data:
            validate_required(data["phone"], "phone")
            validate_max_length(data["phone"], 20, "phone")

        if "email" in data:
            validate_required(data["email"], "email")
            validate_email(data["email"])
            self._ensure_unique_value(
                Provider.email,
                data["email"],
                f"Ya existe un proveedor con el correo '{data['email']}'.",
                exclude_id=provider_id,
            )

        if "address" in data:
            validate_required(data["address"], "address")
            validate_max_length(data["address"], 255, "address")

        return super().update(provider_id, data)

    def delete(self, provider_id: int) -> Provider:
        """Desactiva el proveedor si no tiene productos activos asociados.

        Args:
            provider_id: Identificador del proveedor a desactivar.

        Returns:
            El proveedor desactivado.
        """
        if self._has_active_products(provider_id):
            raise ConflictError(
                "No se puede desactivar el proveedor porque tiene productos activos asociados."
            )
        return super().delete(provider_id)

    def _validate_data(self, data: Dict[str, Any]) -> None:
        """Valida campos obligatorios, longitudes y formato del correo."""
        validate_required(data.get("company_name"), "company_name")
        validate_required(data.get("nit"), "nit")
        validate_required(data.get("phone"), "phone")
        validate_required(data.get("email"), "email")
        validate_required(data.get("address"), "address")

        validate_max_length(data.get("company_name"), 150, "company_name")
        validate_max_length(data.get("nit"), 20, "nit")
        validate_max_length(data.get("phone"), 20, "phone")
        validate_max_length(data.get("email"), 100, "email")
        validate_max_length(data.get("address"), 255, "address")

        validate_email(data["email"])

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
        """Lanza ConflictError si otro registro ya usa ese valor único.

        Args:
            column: Columna única del modelo a verificar (nit o email).
            value: Valor que se quiere usar.
            error_message: Mensaje a lanzar en caso de conflicto.
            exclude_id: Id a excluir de la búsqueda (para actualizaciones).
        """
        query = select(Provider.id).where(column == value)

        if exclude_id is not None:
            query = query.where(Provider.id != exclude_id)

        if self.db.scalar(query) is not None:
            raise ConflictError(error_message)