from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/productos", tags=["Productos"])

@router.post("/", response_model=schemas.ProductoOut, status_code=status.HTTP_201_CREATED)
def crear_producto(producto:schemas.ProductoBase,db:Session=Depends(database.get_db)):
    try:
        resultado = producto_service.crear_producto_service(db,producto)
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409,detail="El NIT o correo del producto ya está registrado")
    except Exception:
        raise HTTPException(status_code=500,detail="Error interno del servidor")

@router.get("/", response_model=list[schemas.ProductoOut])
def mostrar_producto(db:Session=Depends(database.get_db)):
    try:
        return producto_service.mostrar_producto_service(db)
    except Exception:
        raise HTTPException(status_code=500,detail="Error al mostrar producto")

@router.get("/{id}", response_model=schemas.ProductoOut)
def mostrar_por_id(id:int,db:Session=Depends(database.get_db)):
    resultado = producto_service.mostrar_por_id_service(db, id)
    if not resultado:
        raise HTTPException(status_code=404,detail=f"Producto con id {id} no encontrado")
    return resultado

@router.put("/{id}", response_model=schemas.ProductoOut)
def actualizar_producto(id:int,datos=schemas.ProductoBase,db:Session=Depends(database.get_db)):
    try:
        resultado = producto_service.actualizar_producto_service(db,id,datos)
        if not resultado:
            raise HTTPException(status_code=404,detail=f"Producto con id {id} no encontrado")
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409,detail="El NIT o correo ya está en uso")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(id:int,db:Session=Depends(database.get_db)):
    eliminado = producto_service.eliminar_producto_service(db,id)
    if not eliminado:
        raise HTTPException(status_code=404,detail=f"Producto con id {id} no encontrado")
    return None