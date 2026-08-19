from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from app.models.mixins import TimestampMixin

class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    document: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)

    def __repr__(self) -> str:
        return f"<User(id={self.id}, full_name='{self.full_name}', email='{self.email}')>"