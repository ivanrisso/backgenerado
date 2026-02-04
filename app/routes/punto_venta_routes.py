from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.engine import get_db
from app.schemas.punto_venta import PuntoVentaCreate, PuntoVentaResponse, PuntoVentaUpdate
from app.services.punto_venta_service import PuntoVentaService

router = APIRouter(prefix="/puntos-venta", tags=["Puntos de Venta"])

@router.get("/", response_model=List[PuntoVentaResponse])
async def get_puntos_venta(db: AsyncSession = Depends(get_db)):
    return await PuntoVentaService.get_all(db)

@router.post("/", response_model=PuntoVentaResponse, status_code=status.HTTP_201_CREATED)
async def create_punto_venta(data: PuntoVentaCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await PuntoVentaService.create(db, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{id}", response_model=PuntoVentaResponse)
async def get_punto_venta(id: int, db: AsyncSession = Depends(get_db)):
    item = await PuntoVentaService.get_by_id(db, id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Punto de Venta no encontrado")
    return item

@router.put("/{id}", response_model=PuntoVentaResponse)
async def update_punto_venta(id: int, data: PuntoVentaUpdate, db: AsyncSession = Depends(get_db)):
    try:
        item = await PuntoVentaService.update(db, id, data)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Punto de Venta no encontrado")
        return item
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_punto_venta(id: int, db: AsyncSession = Depends(get_db)):
    if not await PuntoVentaService.delete(db, id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Punto de Venta no encontrado")
