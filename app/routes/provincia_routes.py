from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.engine import SessionLocal
from app.services.provincia_service import ProvinciaService
from app.schemas.provincia import ProvinciaCreate, ProvinciaResponse
from typing import AsyncGenerator

router = APIRouter(prefix="/provincias", tags=["Provincia"])

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

@router.get("/", response_model=list[ProvinciaResponse])
async def list_all(db: AsyncSession = Depends(get_db_session)):
    service = ProvinciaService(db)
    return await service.list_all()

@router.get("/{id}", response_model=ProvinciaResponse)
async def get_by_id(id: int, db: AsyncSession = Depends(get_db_session)):
    service = ProvinciaService(db)
    return await service.get_by_id(id)

@router.post("/", response_model=ProvinciaResponse, status_code=status.HTTP_201_CREATED)
async def create(data: ProvinciaCreate, db: AsyncSession = Depends(get_db_session)):
    service = ProvinciaService(db)
    return await service.create(data)