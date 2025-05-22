from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.engine import SessionLocal
from app.services.rolesusuario_service import RolesUsuarioService
from app.schemas.rolesusuario import RolesUsuarioCreate, RolesUsuarioResponse
from typing import AsyncGenerator

router = APIRouter(prefix="/rolesusuarios", tags=["RolesUsuario"])

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

@router.get("/", response_model=list[RolesUsuarioResponse])
async def list_all(db: AsyncSession = Depends(get_db_session)):
    service = RolesUsuarioService(db)
    return await service.list_all()

@router.get("/{id}", response_model=RolesUsuarioResponse)
async def get_by_id(id: int, db: AsyncSession = Depends(get_db_session)):
    service = RolesUsuarioService(db)
    return await service.get_by_id(id)

@router.post("/", response_model=RolesUsuarioResponse, status_code=status.HTTP_201_CREATED)
async def create(data: RolesUsuarioCreate, db: AsyncSession = Depends(get_db_session)):
    service = RolesUsuarioService(db)
    return await service.create(data)