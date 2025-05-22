from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.engine import SessionLocal
from app.services.tipodom_service import TipoDomService
from app.schemas.tipodom import TipoDomCreate, TipoDomResponse
from typing import AsyncGenerator

router = APIRouter(prefix="/tipodoms", tags=["TipoDom"])

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

@router.get("/", response_model=list[TipoDomResponse])
async def list_all(db: AsyncSession = Depends(get_db_session)):
    service = TipoDomService(db)
    return await service.list_all()

@router.get("/{id}", response_model=TipoDomResponse)
async def get_by_id(id: int, db: AsyncSession = Depends(get_db_session)):
    service = TipoDomService(db)
    return await service.get_by_id(id)

@router.post("/", response_model=TipoDomResponse, status_code=status.HTTP_201_CREATED)
async def create(data: TipoDomCreate, db: AsyncSession = Depends(get_db_session)):
    service = TipoDomService(db)
    return await service.create(data)