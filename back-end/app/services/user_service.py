"""Lógica de negocio para los usuarios del sistema."""

from typing import Any, Dict, Optional

from sqlalchemy import select

from app.models import User
from app.services.base_service import BaseService
from app.services.exceptions import (
    ConflictError,
    NotFoundError,
    UnauthorizedError,
)
from app.utils import hash_password, verify_password
from app.services.validators import (
    validate_email,
    validate_max_length,
    validate_min_length,
    validate_required,
)


class UserService(BaseService):
    """Servicio para gestionar usuarios, su contraseña y su autenticación."""

    model = User
    not_found_message = "Usuario no encontrado"

    def create(self, data: Dict[str, Any]) -> User:
        """Crea un usuario nuevo con la contraseña hasheada.

        Args:
            data: Diccionario con full_name, email, document y password plana.

        Returns:
            El usuario creado en la base de datos.
        """
        data = self._normalize(data)

        self._validate_data(data)
        self._ensure_unique_email(data["email"])
        self._ensure_unique_document(data["document"])

        data["hashed_password"] = hash_password(data.pop("password"))

        return super().create(data)

    def update(self, user_id: int, data: Dict[str, Any]) -> User:
        """Actualiza un usuario de forma parcial.

        Si se envía password, la hashea y la guarda como hashed_password.

        Args:
            user_id: Identificador del usuario a actualizar.
            data: Diccionario con los campos que se van a modificar.

        Returns:
            El usuario con los cambios aplicados.
        """
        data = self._normalize(data)

        if "full_name" in data:
            validate_required(data["full_name"], "full_name")
            validate_max_length(data["full_name"], 100, "full_name")

        if "email" in data:
            validate_required(data["email"], "email")
            validate_email(data["email"])
            self._ensure_unique_email(data["email"], exclude_id=user_id)

        if "document" in data:
            validate_required(data["document"], "document")
            validate_max_length(data["document"], 20, "document")
            self._ensure_unique_document(data["document"], exclude_id=user_id)

        if "password" in data:
            validate_required(data["password"], "password")
            validate_min_length(data["password"], 8, "password")
            data["hashed_password"] = hash_password(data.pop("password"))

        return super().update(user_id, data)

    def authenticate(self, email: str, password: str) -> User:
        """Verifica credenciales y devuelve el usuario activo.

        Args:
            email: Correo del usuario.
            password: Contraseña en texto plano a verificar.

        Returns:
            El usuario autenticado.

        Raises:
            UnauthorizedError: Si las credenciales no coinciden o el usuario
                no está activo.
        """
        user = self.db.scalar(select(User).where(User.email == email))

        if user is None or not verify_password(password, user.hashed_password):
            raise UnauthorizedError("Correo o contraseña incorrectos.")

        if not user.is_active:
            raise UnauthorizedError("El usuario no está activo.")

        return user

    def get_by_email(self, email: str) -> User:
        """Devuelve un usuario por su correo o lanza NotFoundError.

        Args:
            email: Correo del usuario a buscar.

        Returns:
            El usuario encontrado.
        """
        user = self.db.scalar(select(User).where(User.email == email))

        if user is None:
            raise NotFoundError(self.not_found_message)

        return user

    # ------------------------------------------------------------------
    # Helpers internos
    # ------------------------------------------------------------------

    def _normalize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Acepta alias cómodos y descarta claves que no deben inyectarse."""
        data = dict(data)

        if "name" in data:
            data["full_name"] = data.pop("name")

        # El hash lo genera siempre el servicio, nunca se recibe de afuera
        data.pop("hashed_password", None)

        return data

    def _validate_data(self, data: Dict[str, Any]) -> None:
        """Valida campos obligatorios, longitudes, correo y contraseña mínima."""
        validate_required(data.get("full_name"), "full_name")
        validate_required(data.get("email"), "email")
        validate_required(data.get("document"), "document")
        validate_required(data.get("password"), "password")

        validate_max_length(data.get("full_name"), 100, "full_name")
        validate_max_length(data.get("email"), 100, "email")
        validate_max_length(data.get("document"), 20, "document")

        validate_email(data["email"])
        validate_min_length(data["password"], 8, "password")

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