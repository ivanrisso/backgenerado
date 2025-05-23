from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.engine import SessionLocal
from app.services.auditoriacomprobante_service import AuditoriaComprobanteService
from app.schemas.auditoria_comprobante import AuditoriaComprobanteCreate, AuditoriaComprobanteResponse
from typing import AsyncGenerator

router = APIRouter(prefix="/auditoriacomprobantes", tags=["AuditoriaComprobante"])

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

@router.get("/", response_model=list[AuditoriaComprobanteResponse])
async def list_all(db: AsyncSession = Depends(get_db_session)):
    service = AuditoriaComprobanteService(db)
    return await service.list_all()

@router.get("/{id}", response_model=AuditoriaComprobanteResponse)
async def get_by_id(id: int, db: AsyncSession = Depends(get_db_session)):
    service = AuditoriaComprobanteService(db)
    return await service.get_by_id(id)

@router.post("/", response_model=AuditoriaComprobanteResponse, status_code=status.HTTP_201_CREATED)
async def create(data: AuditoriaComprobanteCreate, db: AsyncSession = Depends(get_db_session)):
    service = AuditoriaComprobanteService(db)
    return await service.create(data)