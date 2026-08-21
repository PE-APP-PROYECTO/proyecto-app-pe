from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.post("/", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def crear_usuario(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    try:
        resultado = usuario_service.crear_usuario_service(db, user)
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="El correo o documento ya está registrado")
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/", response_model=list[schemas.UserOut])
def mostrar_usuario(db: Session = Depends(database.get_db)):
    try:
        return usuario_service.mostrar_usuario_service(db)
    except Exception:
        raise HTTPException(status_code=500, detail="Error al mostrar usuarios")

@router.get("/{id}", response_model=schemas.UserOut)
def mostrar_por_id(id: int, db: Session = Depends(database.get_db)):
    resultado = usuario_service.mostrar_por_id_service(db, id)
    if not resultado:
        raise HTTPException(status_code=404, detail=f"Usuario con id {id} no encontrado")
    return resultado

@router.put("/{id}", response_model=schemas.UserOut)
def actualizar_usuario(id: int, datos: schemas.UserCreate, db: Session = Depends(database.get_db)):
    try:
        resultado = usuario_service.actualizar_usuario_service(db, id, datos)
        if not resultado:
            raise HTTPException(status_code=404, detail=f"Usuario con id {id} no encontrado")
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="El correo o documento ya está en uso")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(id: int, db: Session = Depends(database.get_db)):
    eliminado = usuario_service.eliminar_usuario_service(db, id)
    if not eliminado:
        raise HTTPException(status_code=404, detail=f"Usuario con id {id} no encontrado")
    return None