from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.engine import SessionLocal
from app.services.rolmenuitem_service import RolMenuItemService
from app.schemas.rolmenuitem import RolMenuItemCreate, RolMenuItemResponse
from typing import AsyncGenerator


router = APIRouter(prefix="/rolmenuitems", tags=["RolMenuItem"])

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

@router.get("/", response_model=list[RolMenuItemResponse])
async def list_all(db: AsyncSession = Depends(get_db_session)):
    service = RolMenuItemService(db)
    return await service.list_all()

@router.get("/{id}", response_model=RolMenuItemResponse)
async def get_by_id(id: int, db: AsyncSession = Depends(get_db_session)):
    service = RolMenuItemService(db)
    return await service.get_by_id(id)

@router.post("/", response_model=RolMenuItemResponse, status_code=status.HTTP_201_CREATED)
async def create(data: RolMenuItemCreate, db: AsyncSession = Depends(get_db_session)):
    service = RolMenuItemService(db)
    return await service.create(data)