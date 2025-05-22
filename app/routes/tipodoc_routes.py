from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.engine import SessionLocal
from app.services.tipodoc_service import TipoDocService
from app.schemas.tipo_doc import TipoDocCreate, TipoDocResponse
from typing import AsyncGenerator


router = APIRouter(prefix="/tipodocs", tags=["TipoDoc"])

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

@router.get("/", response_model=list[TipoDocResponse])
async def list_all(db: AsyncSession = Depends(get_db_session)):
    service = TipoDocService(db)
    return await service.list_all()

@router.get("/{id}", response_model=TipoDocResponse)
async def get_by_id(id: int, db: AsyncSession = Depends(get_db_session)):
    service = TipoDocService(db)
    return await service.get_by_id(id)

@router.post("/", response_model=TipoDocResponse, status_code=status.HTTP_201_CREATED)
async def create(data: TipoDocCreate, db: AsyncSession = Depends(get_db_session)):
    service = TipoDocService(db)
    return await service.create(data)