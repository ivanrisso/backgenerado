from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.engine import SessionLocal
from app.services.comprobantedetalle_service import ComprobanteDetalleService
from app.schemas.comprobante_detalle import ComprobanteDetalleCreate, ComprobanteDetalleResponse
from typing import AsyncGenerator

router = APIRouter(prefix="/comprobantedetalles", tags=["ComprobanteDetalle"])

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
        
@router.get("/", response_model=list[ComprobanteDetalleResponse])
async def list_all(db: AsyncSession = Depends(get_db_session)):
    service = ComprobanteDetalleService(db)
    return await service.list_all()

@router.get("/{id}", response_model=ComprobanteDetalleResponse)
async def get_by_id(id: int, db: AsyncSession = Depends(get_db_session)):
    service = ComprobanteDetalleService(db)
    return await service.get_by_id(id)

@router.post("/", response_model=ComprobanteDetalleResponse, status_code=status.HTTP_201_CREATED)
async def create(data: ComprobanteDetalleCreate, db: AsyncSession = Depends(get_db_session)):
    service = ComprobanteDetalleService(db)
    return await service.create(data)