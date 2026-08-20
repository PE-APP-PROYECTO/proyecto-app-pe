"""Validaciones reutilizables de la capa de servicios."""

import re
from typing import Any

from app.services.exceptions import ValidationError

EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def validate_required(value: Any, field: str) -> None:
    """Verifica que el campo no venga vacío."""
    if value is None or str(value).strip() == "":
        raise ValidationError(f"El campo '{field}' es obligatorio.")


def validate_max_length(value: Any, max_length: int, field: str) -> None:
    """Verifica que el valor no exceda la longitud máxima de la columna."""
    if value is not None and len(str(value)) > max_length:
        raise ValidationError(
            f"El campo '{field}' no puede superar {max_length} caracteres."
        )


def validate_min_length(value: Any, min_length: int, field: str) -> None:
    """Verifica que el valor tenga al menos la longitud mínima."""
    if value is not None and len(str(value)) < min_length:
        raise ValidationError(
            f"El campo '{field}' debe tener al menos {min_length} caracteres."
        )


def validate_email(value: str) -> None:
    """Verifica que el valor tenga formato de correo válido."""
    if not EMAIL_REGEX.match(value.strip()):
        raise ValidationError(f"El correo '{value}' no tiene un formato válido.")


def validate_non_negative(value: Any, field: str) -> None:
    """Verifica que el valor sea numérico y mayor o igual a cero."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        raise ValidationError(f"El campo '{field}' debe ser numérico.")

    if number < 0:
        raise ValidationError(f"El campo '{field}' no puede ser negativo.")


def validate_non_negative_int(value: Any, field: str) -> None:
    """Verifica que el valor sea un entero mayor o igual a cero."""
    try:
        number = int(value)
    except (TypeError, ValueError):
        raise ValidationError(f"El campo '{field}' debe ser un número entero.")

    if number < 0:
        raise ValidationError(f"El campo '{field}' no puede ser negativo.")