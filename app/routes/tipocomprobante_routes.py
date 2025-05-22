from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.engine import SessionLocal
from app.services.tipocomprobante_service import TipoComprobanteService
from app.schemas.tipocomprobante import TipoComprobanteCreate, TipoComprobanteResponse
from typing import AsyncGenerator


router = APIRouter(prefix="/tipocomprobantes", tags=["TipoComprobante"])

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

@router.get("/", response_model=list[TipoComprobanteResponse])
async def list_all(db: AsyncSession = Depends(get_db_session)):
    service = TipoComprobanteService(db)
    return await service.list_all()

@router.get("/{id}", response_model=TipoComprobanteResponse)
async def get_by_id(id: int, db: AsyncSession = Depends(get_db_session)):
    service = TipoComprobanteService(db)
    return await service.get_by_id(id)

@router.post("/", response_model=TipoComprobanteResponse, status_code=status.HTTP_201_CREATED)
async def create(data: TipoComprobanteCreate, db: AsyncSession = Depends(get_db_session)):
    service = TipoComprobanteService(db)
    return await service.create(data)