from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.engine import SessionLocal
from app.services.comprobante_service import ComprobanteService
from app.schemas.comprobante import ComprobanteCreate, ComprobanteResponse
from typing import AsyncGenerator

router = APIRouter(prefix="/comprobantes", tags=["Comprobante"])

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
        
@router.get("/", response_model=list[ComprobanteResponse])
async def list_all(db: AsyncSession = Depends(get_db_session)):
    service = ComprobanteService(db)
    return await service.list_all()

@router.get("/{id}", response_model=ComprobanteResponse)
async def get_by_id(id: int, db: AsyncSession = Depends(get_db_session)):
    service = ComprobanteService(db)
    return await service.get_by_id(id)

@router.post("/", response_model=ComprobanteResponse, status_code=status.HTTP_201_CREATED)
async def create(data: ComprobanteCreate, db: AsyncSession = Depends(get_db_session)):
    service = ComprobanteService(db)
    return await service.create(data)