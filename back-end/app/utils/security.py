"""Utilidades de seguridad para contraseñas."""

import hashlib
import secrets

HASH_ALGORITHM = "sha256"
ITERATIONS = 100_000


def hash_password(password: str) -> str:
    """Convierte una contraseña en un hash seguro."""
    salt = secrets.token_bytes(16)

    derived = hashlib.pbkdf2_hmac(
        HASH_ALGORITHM,
        password.encode("utf-8"),
        salt,
        ITERATIONS
    )

    return "{salt.hex()}${derived.hex()}"


def verify_password(password: str, hashed_password: str) -> bool:
    """Verifica una contraseña contra el hash almacenado."""
    try:
        salt_hex, derived_hex = hashed_password.split("$")
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(derived_hex)
    except (ValueError, AttributeError):
        return False

    derived = hashlib.pbkdf2_hmac(
        HASH_ALGORITHM,
        password.encode("utf-8"),
        salt,
        ITERATIONS
    )

    return secrets.compare_digest(derived, expected)