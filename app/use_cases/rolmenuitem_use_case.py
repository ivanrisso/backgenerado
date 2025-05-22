from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.orm_models import RolMenuItem
from app.repositories.rolmenuitem_repository import RolMenuItemRepository
from app.schemas.rolmenuitem import RolMenuItemCreate

class RolMenuItemUseCase:
    def __init__(self, db: AsyncSession):
        self.repo = RolMenuItemRepository(db)

    async def get_by_id(self, id: int) -> Optional[RolMenuItem]:
        return await self.repo.get_by_id(id)

    async def list_all(self) -> List[RolMenuItem]:
        return await self.repo.list_all()

    async def create(self, data: RolMenuItemCreate) -> RolMenuItem:
        obj = RolMenuItem(**data.model_dump())
        return await self.repo.create(obj)