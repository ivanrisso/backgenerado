from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.engine import SessionLocal
from app.services.usuario_service import UsuarioService
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from typing import AsyncGenerator


router = APIRouter(prefix="/usuarios", tags=["Usuario"])

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

@router.get("/", response_model=list[UsuarioResponse])
async def list_all(db: AsyncSession = Depends(get_db_session)):
    service = UsuarioService(db)
    return await service.list_all()

@router.get("/{id}", response_model=UsuarioResponse)
async def get_by_id(id: int, db: AsyncSession = Depends(get_db_session)):
    service = UsuarioService(db)
    return await service.get_by_id(id)

@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def create(data: UsuarioCreate, db: AsyncSession = Depends(get_db_session)):
    service = UsuarioService(db)
    return await service.create(data)