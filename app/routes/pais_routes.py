from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.engine import SessionLocal
from app.services.pais_service import PaisService
from app.schemas.pais import PaisCreate, PaisResponse
from typing import AsyncGenerator


router = APIRouter(prefix="/paiss", tags=["Pais"])


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

@router.get("/", response_model=list[PaisResponse])
async def list_all(db: AsyncSession = Depends(get_db_session)):
    service = PaisService(db)
    return await service.list_all()

@router.get("/{id}", response_model=PaisResponse)
async def get_by_id(id: int, db: AsyncSession = Depends(get_db_session)):
    service = PaisService(db)
    return await service.get_by_id(id)

@router.post("/", response_model=PaisResponse, status_code=status.HTTP_201_CREATED)
async def create(data: PaisCreate, db: AsyncSession = Depends(get_db_session)):
    service = PaisService(db)
    return await service.create(data)