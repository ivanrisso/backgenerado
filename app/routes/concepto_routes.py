from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.engine import SessionLocal
from app.services.concepto_service import ConceptoService
from app.schemas.concepto import ConceptoCreate, ConceptoResponse
from typing import AsyncGenerator


router = APIRouter(prefix="/conceptos", tags=["Concepto"])

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


@router.get("/", response_model=list[ConceptoResponse])
async def list_all(db: AsyncSession = Depends(get_db_session)):
    service = ConceptoService(db)
    return await service.list_all()

@router.get("/{id}", response_model=ConceptoResponse)
async def get_by_id(id: int, db: AsyncSession = Depends(get_db_session)):
    service = ConceptoService(db)
    return await service.get_by_id(id)

@router.post("/", response_model=ConceptoResponse, status_code=status.HTTP_201_CREATED)
async def create(data: ConceptoCreate, db: AsyncSession = Depends(get_db_session)):
    service = ConceptoService(db)
    return await service.create(data)