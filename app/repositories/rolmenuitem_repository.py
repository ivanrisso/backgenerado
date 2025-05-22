from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from app.infrastructure.db.orm_models import RolMenuItem

class RolMenuItemRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> Optional[RolMenuItem]:
        stmt = select(RolMenuItem).where(RolMenuItem.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_rol_id(self, value) -> Optional[RolMenuItem]:
        stmt = select(RolMenuItem).where(RolMenuItem.rol_id == value)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> List[RolMenuItem]:
        stmt = select(RolMenuItem)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create(self, obj: RolMenuItem) -> RolMenuItem:
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, obj: RolMenuItem) -> None:
        await self.db.delete(obj)
        await self.db.commit()