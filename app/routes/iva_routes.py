from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.engine import SessionLocal
from app.services.iva_service import IvaService
from app.schemas.iva import IvaCreate, IvaResponse
from typing import AsyncGenerator

router = APIRouter(prefix="/ivas", tags=["Iva"])

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

@router.get("/", response_model=list[IvaResponse])
async def list_all(db: AsyncSession = Depends(get_db_session)):
    service = IvaService(db)
    return await service.list_all()

@router.get("/{id}", response_model=IvaResponse)
async def get_by_id(id: int, db: AsyncSession = Depends(get_db_session)):
    service = IvaService(db)
    return await service.get_by_id(id)

@router.post("/", response_model=IvaResponse, status_code=status.HTTP_201_CREATED)
async def create(data: IvaCreate, db: AsyncSession = Depends(get_db_session)):
    service = IvaService(db)
    return await service.create(data)