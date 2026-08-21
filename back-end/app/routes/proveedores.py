from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/proveedores",tags=["Proveedores"])

@router.post("/", response_model=schemas.ProveedorOut, status_code=status.HTTP_201_CREATED)
def crear_proveedor(proveedor:schemas.ProveedorBase, db:Session=Depends(database.get_db)):
    try:
        reusltado = proveedor_service.crear_proveedor_service(db, proveedor)
        return reusltado
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409,detail="El NIT o correo del proveedor ya está registrado")
    except Exception:
        raise HTTPException(status_code=500,detail="Error interno en el servidor")

@router.get("/", response_model=list[schemas.ProveedorOut])
def mostrar_proveedor(db:Session=Depends(database.get_db)):
    try:
        return proveedor_service.mostrar_proveedor_service(db)
    except Exception:
        raise HTTPException(status_code=500,detail="Error al mostrar proveedores")

@router.get("/{id}", response_model=schemas.ProveedorOut)
def mostrar_por_id(id:int,db:Session=Depends(database.get_db)):
    resultado = proveedor_service.mostrar_por_id_service(db,id)
    if not resultado:
        raise HTTPException(status_code=404,detail=f"Proveedor con id {id} no encontrado")
    return resultado

@router.put("/{id}", response_model=schemas.ProveedorOut)
def actualizar_proveedor(id:int,datos=schemas.ProveedorBase,db:Session=Depends(database.get_db)):
    try:
        resultado = proveerdor_service.actualizar_proveedor_service(db,id,datos)
        if not resultado:
            raise HTTPException(satatus_code=404,detail=f"Proveedor con id {id} no encontrado")
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409,detail="El NIT o correo ya está en uso")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_proveedor(id:int,db:Session=Depends(database.get_db)):
    eliminado= proveedor_service.eliminar_proveedor_service(db,id)
    if not eliminado:
        raise HTTPException(status_code=404,detail=f"Proveedor con id {id} no encontrado")
    return None