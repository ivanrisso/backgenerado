from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.engine import SessionLocal
from app.services.tipotel_service import TipoTelService
from app.schemas.tipotel import TipoTelCreate, TipoTelResponse
from typing import AsyncGenerator


router = APIRouter(prefix="/tipotels", tags=["TipoTel"])

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

@router.get("/", response_model=list[TipoTelResponse])
async def list_all(db: AsyncSession = Depends(get_db_session)):
    service = TipoTelService(db)
    return await service.list_all()

@router.get("/{id}", response_model=TipoTelResponse)
async def get_by_id(id: int, db: AsyncSession = Depends(get_db_session)):
    service = TipoTelService(db)
    return await service.get_by_id(id)

@router.post("/", response_model=TipoTelResponse, status_code=status.HTTP_201_CREATED)
async def create(data: TipoTelCreate, db: AsyncSession = Depends(get_db_session)):
    service = TipoTelService(db)
    return await service.create(data)