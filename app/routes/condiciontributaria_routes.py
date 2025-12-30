from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.infrastructure.db.engine import get_db
from app.repositories.condiciontributaria_repository import CondicionTributariaRepositoryImpl
from app.schemas.condicion_tributaria import CondicionTributariaCreate, CondicionTributariaUpdate, CondicionTributariaResponse
from app.domain.entities.condiciontributaria import CondicionTributaria

router = APIRouter(prefix="/condiciones-tributarias", tags=["Condiciones Tributarias"])

@router.get("/", response_model=List[CondicionTributariaResponse])
async def get_all(db: AsyncSession = Depends(get_db)):
    repo = CondicionTributariaRepositoryImpl(db)
    return await repo.get_all()

@router.get("/{id}", response_model=CondicionTributariaResponse)
async def get_by_id(id: int, db: AsyncSession = Depends(get_db)):
    repo = CondicionTributariaRepositoryImpl(db)
    condicion = await repo.get_by_id(id)
    if not condicion:
        raise HTTPException(status_code=404, detail="Condición tributaria no encontrada")
    return condicion

@router.post("/", response_model=CondicionTributariaResponse)
async def create(data: CondicionTributariaCreate, db: AsyncSession = Depends(get_db)):
    repo = CondicionTributariaRepositoryImpl(db)
    entity = CondicionTributaria(nombre=data.nombre, descripcion=data.descripcion)
    return await repo.create(entity)

@router.patch("/{id}", response_model=CondicionTributariaResponse)
async def update(id: int, data: CondicionTributariaUpdate, db: AsyncSession = Depends(get_db)):
    repo = CondicionTributariaRepositoryImpl(db)
    # Note: To be strict we should fetch first, but repo handles existence check
    entity = CondicionTributaria(nombre=data.nombre, descripcion=data.descripcion)
    return await repo.update(id, entity)

@router.delete("/{id}")
async def delete(id: int, db: AsyncSession = Depends(get_db)):
    repo = CondicionTributariaRepositoryImpl(db)
    await repo.delete(id)
    return {"message": "Condición tributaria eliminada"}
