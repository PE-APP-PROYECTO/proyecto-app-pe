from typing import Annotated
from fastapi import APIRouter, Depends

# Importas la dependencia y el modelo desde la nueva carpeta
from app.core.login import get_current_user_with_role, UserPayload

router = APIRouter()

@router.get("/dashboard")
def dashboard(
    current_user: Annotated[UserPayload, Depends(get_current_user_with_role(["admin", "user"]))]
):
    return {"mensaje": f"Bienvenido {current_user.username}"}