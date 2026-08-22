"""Excepciones personalizadas de la capa de servicios.

Permiten que los servicios reporten errores de negocio
sin depender de HTTP ni del framework web.
"""


class ServiceError(Exception):
    """Error base de todos los servicios."""

    status_code: int = 400

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class NotFoundError(ServiceError):
    """El registro solicitado no existe."""

    status_code = 404

    def __init__(self, message: str = "Recurso no encontrado"):
        super().__init__(message)


class ValidationError(ServiceError):
    """Los datos no cumplen las reglas de negocio."""

    status_code = 422

    def __init__(self, message: str = "Datos inválidos"):
        super().__init__(message)


class ConflictError(ServiceError):
    """La operación entra en conflicto con datos existentes."""

    status_code = 409

    def __init__(self, message: str = "Conflicto con datos existentes"):
        super().__init__(message)


class UnauthorizedError(ServiceError):
    """Credenciales inválidas o usuario inactivo."""

    status_code = 401

    def __init__(self, message: str = "No autorizado"):
        super().__init__(message)