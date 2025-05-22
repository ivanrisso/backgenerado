from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.use_cases.rolmenuitem_use_case import RolMenuItemUseCase
from app.schemas.rolmenuitem import RolMenuItemCreate
from app.domain.rolmenuitem import RolMenuItem

class RolMenuItemService:
    def __init__(self, db: AsyncSession):
        self.use_case = RolMenuItemUseCase(db)

    async def get_by_id(self, id: int) -> Optional[RolMenuItem]:
        return await self.use_case.get_by_id(id)

    async def list_all(self) -> List[RolMenuItem]:
        return await self.use_case.list_all()

    async def create(self, data: RolMenuItemCreate) -> RolMenuItem:
        return await self.use_case.create(data)