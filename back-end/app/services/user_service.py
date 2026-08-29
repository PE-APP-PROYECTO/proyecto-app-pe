"""Lógica de negocio para los usuarios del sistema."""

from typing import List, Optional
from sqlalchemy import select

from app.models import User
from app.schemas.user import UsuarioCreateSchema, UserUpdateSchema, PasswordUpdateSchema
from app.services.base_service import BaseService
from app.utils import (
    ConflictError,
    NotFoundError,
    UnauthorizedError,
    hash_password,
    verify_password,
)


class UserService(BaseService):
    """Servicio para gestionar usuarios, su contraseña y su autenticación."""

    model = User
    not_found_message = "Usuario no encontrado"

    def create(self, schema: UsuarioCreateSchema) -> User:
        """Crea un usuario nuevo descartando confirm_password y hasheando el password."""
        self._ensure_unique_email(schema.email)
        self._ensure_unique_document(schema.document)

        # Convertimos a dict y descartamos la confirmación de contraseña
        user_data = schema.model_dump()
        user_data.pop("confirm_password", None)

        # Mapeamos 'fullName' del schema al 'full_name' del modelo SQLAlchemy si usas snake_case en BD
        if "fullName" in user_data:
            user_data["full_name"] = user_data.pop("fullName")

        user_data["hashed_password"] = hash_password(user_data.pop("password"))

        return super().create(user_data)

    def update(self, user_id: int, schema: UserUpdateSchema) -> User:
        """Actualiza la información del perfil del usuario."""
        update_data = schema.model_dump(exclude_unset=True)

        if not update_data:
            return self.get_by_id(user_id)

        if "fullName" in update_data:
            update_data["full_name"] = update_data.pop("fullName")

        if "email" in update_data:
            self._ensure_unique_email(update_data["email"], exclude_id=user_id)

        if "document" in update_data:
            self._ensure_unique_document(update_data["document"], exclude_id=user_id)

        return super().update(user_id, update_data)

    def change_password(self, user_id: int, schema: PasswordUpdateSchema) -> None:
        """Verifica la contraseña actual y actualiza por la nueva."""
        user = self.get_by_id(user_id)

        # Validar contraseña actual contra la BD
        if not verify_password(schema.current_password, user.hashed_password):
            raise UnauthorizedError("La contraseña actual es incorrecta.")

        # Guardar la nueva contraseña encriptada
        user.hashed_password = hash_password(schema.new_password)
        self.db.commit()

    def list(self) -> List[User]:
        """Obtiene la lista de todos los usuarios."""
        query = select(User)
        return self.db.scalars(query).all()

    def authenticate(self, email: str, password: str) -> User:
        """Verifica credenciales y devuelve el usuario activo."""
        user = self.db.scalar(select(User).where(User.email == email))

        if user is None or not verify_password(password, user.hashed_password):
            raise UnauthorizedError("Correo o contraseña incorrectos.")

        if not user.is_active:
            raise UnauthorizedError("El usuario no está activo.")

        return user

    def get_by_email(self, email: str) -> User:
        """Devuelve un usuario por su correo o lanza NotFoundError."""
        user = self.db.scalar(select(User).where(User.email == email))

        if user is None:
            raise NotFoundError(self.not_found_message)

        return user

    # ------------------------------------------------------------------
    # Helpers internos
    # ------------------------------------------------------------------

    def _ensure_unique_email(
        self, email: str, exclude_id: Optional[int] = None
    ) -> None:
        """Lanza ConflictError si ya existe otro usuario con el mismo correo."""
        query = select(User.id).where(User.email == email)

        if exclude_id is not None:
            query = query.where(User.id != exclude_id)

        if self.db.scalar(query) is not None:
            raise ConflictError(f"Ya existe un usuario con el correo '{email}'.")

    def _ensure_unique_document(
        self, document: str, exclude_id: Optional[int] = None
    ) -> None:
        """Lanza ConflictError si ya existe otro usuario con el mismo documento."""
        query = select(User.id).where(User.document == document)

        if exclude_id is not None:
            query = query.where(User.id != exclude_id)

        if self.db.scalar(query) is not None:
            raise ConflictError(
                f"Ya existe un usuario con el documento '{document}'."
            )
