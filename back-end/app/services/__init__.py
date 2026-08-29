"""Módulo de servicios de la aplicación.

Expone los servicios que usan las rutas y controladores del backend
para operar sobre usuarios, marcas, proveedores y productos
sin tocar directamente la base de datos ni la lógica HTTP.
"""

from app.services.base_service import BaseService
from app.services.brand_service import BrandService
from app.services.provider_service import ProviderService
from app.services.product_service import ProductService
from app.services.user_service import UserService

__all__ = [
    "BaseService",
    "BrandService",
    "ProviderService",
    "ProductService",
    "UserService",
]