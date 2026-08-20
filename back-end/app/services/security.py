"""Hash de contraseñas con librería estándar.

Usa PBKDF2-HMAC-SHA256 con salt aleatorio para que el equipo
no necesite instalar dependencias externas nuevas.
"""

import hashlib
import secrets

HASH_ALGORITHM = "sha256"
ITERATIONS = 100_000


def hash_password(password: str) -> str:
    """Convierte una contraseña plana en un hash con salt aleatorio."""
    salt = secrets.token_bytes(16)
    derived = hashlib.pbkdf2_hmac(
        HASH_ALGORITHM, password.encode("utf-8"), salt, ITERATIONS
    )
    return f"{salt.hex()}${derived.hex()}"


def verify_password(password: str, hashed_password: str) -> bool:
    """Compara una contraseña plana contra el hash almacenado."""
    try:
        salt_hex, derived_hex = hashed_password.split("$")
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(derived_hex)
    except (ValueError, AttributeError):
        return False

    derived = hashlib.pbkdf2_hmac(
        HASH_ALGORITHM, password.encode("utf-8"), salt, ITERATIONS
    )
    return secrets.compare_digest(derived, expected)