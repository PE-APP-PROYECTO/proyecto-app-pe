from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/marcas", tags=["Marcas"])

@router.post("/", response_model=schemas.MarcaOut, status_code=status.HTTP_201_CREATED)
def crear_marca(marca: schemas.MarcaBase, db: Session = Depends(database.get_db)):
    try:
        resultado = marca_service.crear_marca_service(db, marca)
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="El nombre de la marca ya está registrado")
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/", response_model=list[schemas.MarcaOut])
def listar_marcas(db: Session = Depends(database.get_db)):
    try:
        return marca_service.listar_marcas_service(db)
    except Exception:
        raise HTTPException(status_code=500, detail="Error al listar marcas")

@router.get("/{id}", response_model=schemas.MarcaOut)
def mostrar_por_id(id: int, db: Session = Depends(database.get_db)):
    resultado = marca_service.obtener_marca_service(db, id)
    if not resultado:
        raise HTTPException(status_code=404, detail=f"Marca con id {id} no encontrada")
    return resultado

@router.put("/{id}", response_model=schemas.MarcaOut)
def actualizar_marca(id: int, datos: schemas.MarcaBase, db: Session = Depends(database.get_db)):
    try:
        resultado = marca_service.actualizar_marca_service(db, id, datos)
        if not resultado:
            raise HTTPException(status_code=404, detail=f"Marca con id {id} no encontrada")
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="El nombre de la marca ya existe")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_marca(id: int, db: Session = Depends(database.get_db)):
    eliminado = marca_service.eliminar_marca_service(db, id)
    if not eliminado:
        raise HTTPException(status_code=404, detail=f"Marca con id {id} no encontrada")
    return None