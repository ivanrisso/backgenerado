from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.use_cases.menuitem_use_case import MenuItemUseCase
from app.schemas.menu_item import MenuItemCreate
from app.infrastructure.db.orm_models import MenuItem

class MenuItemService:
    def __init__(self, db: AsyncSession):
        self.use_case = MenuItemUseCase(db)

    async def get_by_id(self, id: int) -> Optional[MenuItem]:
        return await self.use_case.get_by_id(id)

    async def list_all(self) -> List[MenuItem]:
        return await self.use_case.list_all()

    async def create(self, data: MenuItemCreate) -> MenuItem:
        return await self.use_case.create(data)