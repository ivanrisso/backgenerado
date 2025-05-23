from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.engine import SessionLocal
from app.services.clienteimpuesto_service import ClienteImpuestoService
from app.schemas.clienteimpuesto import ClienteImpuestoCreate, ClienteImpuestoResponse
from typing import AsyncGenerator

router = APIRouter(prefix="/clienteimpuestos", tags=["ClienteImpuesto"])

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

@router.get("/", response_model=list[ClienteImpuestoResponse])
async def list_all(db: AsyncSession = Depends(get_db_session)):
    service = ClienteImpuestoService(db)
    return await service.list_all()

@router.get("/{id}", response_model=ClienteImpuestoResponse)
async def get_by_id(id: int, db: AsyncSession = Depends(get_db_session)):
    service = ClienteImpuestoService(db)
    return await service.get_by_id(id)

@router.post("/", response_model=ClienteImpuestoResponse, status_code=status.HTTP_201_CREATED)
async def create(data: ClienteImpuestoCreate, db: AsyncSession = Depends(get_db_session)):
    service = ClienteImpuestoService(db)
    return await service.create(data)