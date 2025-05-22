from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.engine import SessionLocal
from app.services.cuentacorriente_service import CuentaCorrienteService
from app.schemas.cuenta_corriente import CuentaCorrienteCreate, CuentaCorrienteResponse
from typing import AsyncGenerator


router = APIRouter(prefix="/cuentacorrientes", tags=["CuentaCorriente"])

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

@router.get("/", response_model=list[CuentaCorrienteResponse])
async def list_all(db: AsyncSession = Depends(get_db_session)):
    service = CuentaCorrienteService(db)
    return await service.list_all()

@router.get("/{id}", response_model=CuentaCorrienteResponse)
async def get_by_id(id: int, db: AsyncSession = Depends(get_db_session)):
    service = CuentaCorrienteService(db)
    return await service.get_by_id(id)

@router.post("/", response_model=CuentaCorrienteResponse, status_code=status.HTTP_201_CREATED)
async def create(data: CuentaCorrienteCreate, db: AsyncSession = Depends(get_db_session)):
    service = CuentaCorrienteService(db)
    return await service.create(data)