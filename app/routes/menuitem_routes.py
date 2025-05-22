from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.engine import SessionLocal
from app.services.menuitem_service import MenuItemService
from app.schemas.menu_item import MenuItemCreate, MenuItemResponse
from typing import AsyncGenerator

router = APIRouter(prefix="/menuitems", tags=["MenuItem"])

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

@router.get("/", response_model=list[MenuItemResponse])
async def list_all(db: AsyncSession = Depends(get_db_session)):
    service = MenuItemService(db)
    return await service.list_all()

@router.get("/{id}", response_model=MenuItemResponse)
async def get_by_id(id: int, db: AsyncSession = Depends(get_db_session)):
    service = MenuItemService(db)
    return await service.get_by_id(id)

@router.post("/", response_model=MenuItemResponse, status_code=status.HTTP_201_CREATED)
async def create(data: MenuItemCreate, db: AsyncSession = Depends(get_db_session)):
    service = MenuItemService(db)
    return await service.create(data)