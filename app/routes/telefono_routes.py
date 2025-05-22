from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.engine import SessionLocal
from app.services.telefono_service import TelefonoService
from app.schemas.telefono import TelefonoCreate, TelefonoResponse
from typing import AsyncGenerator

router = APIRouter(prefix="/telefonos", tags=["Telefono"])

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

@router.get("/", response_model=list[TelefonoResponse])
async def list_all(db: AsyncSession = Depends(get_db_session)):
    service = TelefonoService(db)
    return await service.list_all()

@router.get("/{id}", response_model=TelefonoResponse)
async def get_by_id(id: int, db: AsyncSession = Depends(get_db_session)):
    service = TelefonoService(db)
    return await service.get_by_id(id)

@router.post("/", response_model=TelefonoResponse, status_code=status.HTTP_201_CREATED)
async def create(data: TelefonoCreate, db: AsyncSession = Depends(get_db_session)):
    service = TelefonoService(db)
    return await service.create(data)