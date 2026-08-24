from datetime import datetime, timedelta, timezone
from typing  import Annotated
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from app.config import settings
from app.schemas.token import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Generación de Token JWT ---
def  create_access_token(data: dict, expires_delta: timedelta | None = None)-> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

# --- Fabrica de Dependencias (Capa de Autenticación y Autorización) ---
def get_current_user_with_role(allowed_roles: list[str]):
    """
    Retorna una función de dependencia que FastAPI ejecuta automáticamente.
    Valida la firma, la expiración del JWT y los roles de acceso.
    """
    def dependency(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenData:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(
                token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
            )
            username: str | None = payload.get("sub")
            role: str | None = payload.get("role")

            if username is None or role is None:
                raise credentials_exception

        except jwt.PyJWTError:
            raise credentials_exception

        if role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes los permisos necesarios para acceder a este recurso",
            )
    
        return TokenData(username=username, role=role)

    return dependency





