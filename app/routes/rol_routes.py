from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.engine import SessionLocal
from app.services.rol_service import RolService
from app.schemas.rol import RolCreate, RolResponse
from typing import AsyncGenerator

router = APIRouter(prefix="/rols", tags=["Rol"])

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

@router.get("/", response_model=list[RolResponse])
async def list_all(db: AsyncSession = Depends(get_db_session)):
    service = RolService(db)
    return await service.list_all()

@router.get("/{id}", response_model=RolResponse)
async def get_by_id(id: int, db: AsyncSession = Depends(get_db_session)):
    service = RolService(db)
    return await service.get_by_id(id)

@router.post("/", response_model=RolResponse, status_code=status.HTTP_201_CREATED)
async def create(data: RolCreate, db: AsyncSession = Depends(get_db_session)):
    service = RolService(db)
    return await service.create(data)