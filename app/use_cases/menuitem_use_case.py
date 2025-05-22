from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.orm_models import MenuItem
from app.repositories.menuitem_repository import MenuItemRepository
from app.domain.menuitem import MenuItem
from app.schemas.menu_item import MenuItemCreate

class MenuItemUseCase:
    def __init__(self, db: AsyncSession):
        self.repo = MenuItemRepository(db)

    async def get_by_id(self, id: int) -> Optional[MenuItem]:
        return await self.repo.get_by_id(id)

    async def list_all(self) -> List[MenuItem]:
        return await self.repo.list_all()

    async def create(self, data: MenuItemCreate) -> MenuItem:
        obj = MenuItem(**data.model_dump())
        return await self.repo.create(obj)