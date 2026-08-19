from typing import TYPE_CHECKING, List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.product import Product

class Provider(TimestampMixin, Base):
    """Representa un proveedor externo de productos."""

    __tablename__ = "providers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    company_name: Mapped[str] = mapped_column(String(150), nullable=False)
    nit: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    products: Mapped[List["Product"]] = relationship(back_populates="provider")

    def __repr__(self) -> str:
        return f"<Provider(id={self.id}, company_name='{self.company_name}', nit='{self.nit}')>"
