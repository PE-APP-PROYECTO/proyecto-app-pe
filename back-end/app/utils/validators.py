"""Validaciones reutilizables de la capa de servicios.

Agrupa funciones que verifican los datos recibidos por los servicios
antes de que lleguen a la base de datos, lanzando ``ValidationError``
cuando alguna regla no se cumple.
"""

import re
from typing import Any

from app.utils.exceptions import ValidationError

EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def validate_required(value: Any, field: str) -> None:
    """Verifica que un campo no venga vacío.

    Args:
        value: Valor recibido para el campo.
        field: Nombre del campo, usado en el mensaje de error.

    Raises:
        ValidationError: Si el valor es None o está vacío.
    """
    if value is None or str(value).strip() == "":
        raise ValidationError(f"El campo '{field}' es obligatorio.")


def validate_max_length(value: Any, max_length: int, field: str) -> None:
    """Verifica que el valor no exceda la longitud máxima de la columna.

    Args:
        value: Valor a revisar.
        max_length: Cantidad máxima de caracteres permitidos.
        field: Nombre del campo, usado en el mensaje de error.

    Raises:
        ValidationError: Si el valor supera la longitud máxima.
    """
    if value is not None and len(str(value)) > max_length:
        raise ValidationError(
            f"El campo '{field}' no puede superar {max_length} caracteres."
        )


def validate_min_length(value: Any, min_length: int, field: str) -> None:
    """Verifica que el valor tenga al menos la longitud mínima.

    Args:
        value: Valor a revisar.
        min_length: Cantidad mínima de caracteres requerida.
        field: Nombre del campo, usado en el mensaje de error.

    Raises:
        ValidationError: Si el valor es más corto que la longitud mínima.
    """
    if value is not None and len(str(value)) < min_length:
        raise ValidationError(
            f"El campo '{field}' debe tener al menos {min_length} caracteres."
        )


def validate_email(value: str) -> None:
    """Verifica que el valor tenga formato de correo válido.

    Args:
        value: Texto a validar como correo electrónico.

    Raises:
        ValidationError: Si el formato no coincide con la expresión regular.
    """
    if not EMAIL_REGEX.match(value.strip()):
        raise ValidationError(f"El correo '{value}' no tiene un formato válido.")


def validate_non_negative(value: Any, field: str) -> None:
    """Verifica que el valor sea numérico y mayor o igual a cero.

    Args:
        value: Valor a convertir a flotante y revisar.
        field: Nombre del campo, usado en el mensaje de error.

    Raises:
        ValidationError: Si el valor no es numérico o es negativo.
    """
    try:
        number = float(value)
    except (TypeError, ValueError):
        raise ValidationError(f"El campo '{field}' debe ser numérico.")

    if number < 0:
        raise ValidationError(f"El campo '{field}' no puede ser negativo.")


def validate_non_negative_int(value: Any, field: str) -> None:
    """Verifica que el valor sea un entero mayor o igual a cero.

    Args:
        value: Valor a convertir a entero y revisar.
        field: Nombre del campo, usado en el mensaje de error.

    Raises:
        ValidationError: Si el valor no es entero o es negativo.
    """
    try:
        number = int(value)
    except (TypeError, ValueError):
        raise ValidationError(f"El campo '{field}' debe ser un número entero.")

    if number < 0:
        raise ValidationError(f"El campo '{field}' no puede ser negativo.")