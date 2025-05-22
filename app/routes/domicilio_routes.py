from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.engine import SessionLocal
from app.services.domicilio_service import DomicilioService
from app.schemas.domicilio import DomicilioCreate, DomicilioResponse
from typing import AsyncGenerator


router = APIRouter(prefix="/domicilios", tags=["Domicilio"])


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

@router.get("/", response_model=list[DomicilioResponse])
async def list_all(db: AsyncSession = Depends(get_db_session)):
    service = DomicilioService(db)
    return await service.list_all()

@router.get("/{id}", response_model=DomicilioResponse)
async def get_by_id(id: int, db: AsyncSession = Depends(get_db_session)):
    service = DomicilioService(db)
    return await service.get_by_id(id)

@router.post("/", response_model=DomicilioResponse, status_code=status.HTTP_201_CREATED)
async def create(data: DomicilioCreate, db: AsyncSession = Depends(get_db_session)):
    service = DomicilioService(db)
    return await service.create(data)