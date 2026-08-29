from typing import Any, Dict, List, Optional
from sqlalchemy import or_, select

from app.models import Brand, Product, Provider
from app.schemas.product import CreateProductSchema, UpdateProductSchema
from app.services.base_service import BaseService
from app.utils import ConflictError, ValidationError

class ProductService(BaseService):
    """Servicio para gestionar productos con filtros y reglas de negocio."""

    model = Product
    not_found_message = "Producto no encontrado"

    def create(self, schema: CreateProductSchema) -> Product:
        """Crea un producto nuevo validando datos, referencia y relaciones.
        Args:
            data: Diccionario con los datos del producto.
        Returns:
            El producto creado en la base de datos.
        """
        self._ensure_unique_reference(schema.reference)
        self._ensure_brand_exists(schema.brand_id)
        self._ensure_provider_exists(schema.provider_id)

        return super().create(schema.model_dump())

    def update(self, product_id: int, schema: UpdateProductSchema) -> Product:
        """Actualiza un producto de forma parcial.
        Args:
            product_id: Identificador del producto a actualizar.
            data: Diccionario con los campos que se van a modificar.
        Returns:
            El producto con los cambios aplicados.
        """
        update_date = schema.model_dump(exclude_unset=True)

        if not update_date:
          return self.get_by_id(product_id)

        if "reference" in update_date:
            self._ensure_unique_reference(update_date["reference"], exclude_id=product_id)

        if "brand_id" in update_date:
            self._ensure_brand_exists(update_date["brand_id"])

        if "provider_id" in update_date:
            self._ensure_provider_exists(update_date["provider_id"])

        return super().update(product_id, update_date)

    def list(
        self,
        skip: int = 0,
        limit: int = 100,
        only_active: bool = True,
        search: Optional[str] = None,
        brand_id: Optional[int] = None,
        provider_id: Optional[int] = None,
    ) -> List[Product]:
        """Lista productos con búsqueda y filtros por marca/proveedor.
        Args:
            skip: Cantidad de registros a omitir (paginación).
            limit: Cantidad máxima de registros a devolver.
            only_active: Si es True, devuelve solo productos activos.
            search: Texto libre para buscar en referencia, descripción o color.
            brand_id: Filtra productos de una marca específica.
            provider_id: Filtra productos de un proveedor específico.
        Returns:
            Lista de productos que cumplen los criterios.
        """
        query = select(Product)

        if only_active:
            query = query.where(Product.is_active.is_(True))

        if search:
            pattern = f"%{search}%"
            query = query.where(
                or_(
                    Product.reference.ilike(pattern),
                    Product.description.ilike(pattern),
                    Product.color.ilike(pattern),
                )
            )

        if brand_id is not None:
            query = query.where(Product.brand_id == brand_id)

        if provider_id is not None:
            query = query.where(Product.provider_id == provider_id)

        query = query.offset(skip).limit(limit)
        return self.db.scalars(query).all()

    def get_dataset_for_ai(self) -> List[Dict[str, Any]]:
        """Devuelve los productos activos en formato útil para el equipo de IA."""
        products = self.list(limit=1000, only_active=True)

        return [
            {
                "id": p.id,
                "reference": p.reference,
                "price": float(p.price),
                "color": p.color,
                "stock": p.stock,
                "brand_id": p.brand_id,
                "provider_id": p.provider_id,
            }
            for p in products
        ]

    # ------------------------------------------------------------------
    # Helpers internos
    # ------------------------------------------------------------------

    def _ensure_unique_reference(
        self, reference: str, exclude_id: Optional[int] = None
    ) -> None:
        """Lanza ConflictError si ya existe otro producto con la misma referencia."""
        query = select(Product.id).where(Product.reference == reference)

        if exclude_id is not None:
            query = query.where(Product.id != exclude_id)

        if self.db.scalar(query) is not None:
            raise ConflictError(
                f"Ya existe un producto con la referencia '{reference}'."
            )

    def _ensure_brand_exists(self, brand_id: int) -> None:
        """Lanza ValidationError si la marca no existe o no está activa."""
        brand = self.db.get(Brand, brand_id)

        if brand is None or not brand.is_active:
            raise ValidationError("La marca indicada no existe o no está activa.")

    def _ensure_provider_exists(self, provider_id: int) -> None:
        """Lanza ValidationError si el proveedor no existe o no está activo."""
        provider = self.db.get(Provider, provider_id)

        if provider is None or not provider.is_active:
            raise ValidationError("El proveedor indicado no existe o no está activo.")
