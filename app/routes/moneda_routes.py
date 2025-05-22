from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.engine import SessionLocal
from app.services.moneda_service import MonedaService
from app.schemas.moneda import MonedaCreate, MonedaResponse
from typing import AsyncGenerator


router = APIRouter(prefix="/monedas", tags=["Moneda"])

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

@router.get("/", response_model=list[MonedaResponse])
async def list_all(db: AsyncSession = Depends(get_db_session)):
    service = MonedaService(db)
    return await service.list_all()

@router.get("/{id}", response_model=MonedaResponse)
async def get_by_id(id: int, db: AsyncSession = Depends(get_db_session)):
    service = MonedaService(db)
    return await service.get_by_id(id)

@router.post("/", response_model=MonedaResponse, status_code=status.HTTP_201_CREATED)
async def create(data: MonedaCreate, db: AsyncSession = Depends(get_db_session)):
    service = MonedaService(db)
    return await service.create(data)