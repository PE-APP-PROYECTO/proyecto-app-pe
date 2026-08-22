"""Hash de contraseñas con librería estándar.

Usa PBKDF2-HMAC-SHA256 con un salt aleatorio para que el equipo
no necesite instalar dependencias externas nuevas.
El formato almacenado es ``salt_hex$derived_hex``.
"""

import hashlib
import secrets

HASH_ALGORITHM = "sha256"
ITERATIONS = 100_000


def hash_password(password: str) -> str:
    """Convierte una contraseña plana en un hash con salt aleatorio.

    Args:
        password: Contraseña en texto plano.

    Returns:
        Cadena con el formato ``salt_hex$derived_hex`` lista para almacenar.
    """
    salt = secrets.token_bytes(16)
    derived = hashlib.pbkdf2_hmac(
        HASH_ALGORITHM, password.encode("utf-8"), salt, ITERATIONS
    )
    return f"{salt.hex()}${derived.hex()}"


def verify_password(password: str, hashed_password: str) -> bool:
    """Compara una contraseña plana contra el hash almacenado.

    Args:
        password: Contraseña en texto plano a verificar.
        hashed_password: Hash generado previamente por ``hash_password``.

    Returns:
        True si la contraseña coincide con el hash; False en caso
        contrario o si el formato almacenado es inválido.
    """
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