from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.engine import SessionLocal
from app.services.operador_service import OperadorService
from app.schemas.operador import OperadorCreate, OperadorResponse
from typing import AsyncGenerator


router = APIRouter(prefix="/operadors", tags=["Operador"])

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

@router.get("/", response_model=list[OperadorResponse])
async def list_all(db: AsyncSession = Depends(get_db_session)):
    service = OperadorService(db)
    return await service.list_all()

@router.get("/{id}", response_model=OperadorResponse)
async def get_by_id(id: int, db: AsyncSession = Depends(get_db_session)):
    service = OperadorService(db)
    return await service.get_by_id(id)

@router.post("/", response_model=OperadorResponse, status_code=status.HTTP_201_CREATED)
async def create(data: OperadorCreate, db: AsyncSession = Depends(get_db_session)):
    service = OperadorService(db)
    return await service.create(data)