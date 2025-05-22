from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.engine import SessionLocal
from app.services.tipoimpuesto_service import TipoImpuestoService
from app.schemas.tipo_impuesto import TipoImpuestoCreate, TipoImpuestoResponse
from typing import AsyncGenerator


router = APIRouter(prefix="/tipoimpuestos", tags=["TipoImpuesto"])

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

@router.get("/", response_model=list[TipoImpuestoResponse])
async def list_all(db: AsyncSession = Depends(get_db_session)):
    service = TipoImpuestoService(db)
    return await service.list_all()

@router.get("/{id}", response_model=TipoImpuestoResponse)
async def get_by_id(id: int, db: AsyncSession = Depends(get_db_session)):
    service = TipoImpuestoService(db)
    return await service.get_by_id(id)

@router.post("/", response_model=TipoImpuestoResponse, status_code=status.HTTP_201_CREATED)
async def create(data: TipoImpuestoCreate, db: AsyncSession = Depends(get_db_session)):
    service = TipoImpuestoService(db)
    return await service.create(data)