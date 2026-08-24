from typing import Annotated
from fastapi import FastAPI,HTTPException, Depends, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext

from app.config import settings
from app.core.login import  create_access_token
from app.schemas.token import Token, LoginRequest

router = APIRouter(prefix="/token", tags=["Token"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("", response_model=Token ,status_code=status.HTTP_200_OK)
def login(payload: LoginRequest):
    is_user_ok = payload.username == settings.ADMIN_USER 
    is_pass_ok = pwd_context.verify(payload.password, settings.ADMIN_PASSWORD_HASH)
    if not(is_user_ok and is_pass_ok) :
        raise HTTPException(
            status_code=400, 
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token = create_access_token(
        data={
            "sub": payload.username,
            "role": "admin"
        }
    )

    return {"access_token": access_token, "token_type": "bearer"}