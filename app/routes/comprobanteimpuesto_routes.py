from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.engine import SessionLocal
from app.services.comprobanteimpuesto_service import ComprobanteImpuestoService
from app.schemas.comprobante_impuesto import ComprobanteImpuestoCreate, ComprobanteImpuestoResponse
from typing import AsyncGenerator


router = APIRouter(prefix="/comprobanteimpuestos", tags=["ComprobanteImpuesto"])

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

@router.get("/", response_model=list[ComprobanteImpuestoResponse])
async def list_all(db: AsyncSession = Depends(get_db_session)):
    service = ComprobanteImpuestoService(db)
    return await service.list_all()

@router.get("/{id}", response_model=ComprobanteImpuestoResponse)
async def get_by_id(id: int, db: AsyncSession = Depends(get_db_session)):
    service = ComprobanteImpuestoService(db)
    return await service.get_by_id(id)

@router.post("/", response_model=ComprobanteImpuestoResponse, status_code=status.HTTP_201_CREATED)
async def create(data: ComprobanteImpuestoCreate, db: AsyncSession = Depends(get_db_session)):
    service = ComprobanteImpuestoService(db)
    return await service.create(data)