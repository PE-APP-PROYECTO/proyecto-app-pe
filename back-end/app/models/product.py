from sqlalchemy import String, Numeric, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from app.models.mixins import TimestampMixin

class Product(TimestampMixin, Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    reference: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    color: Mapped[str] = mapped_column(String(50), nullable=False)
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, default=0)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    provider_id: Mapped[int] = mapped_column(ForeignKey("providers.id"), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    def __repr__(self) -> str:
        return f"<Product(id={self.id}, reference='{self.reference}', price={self.price})>"
