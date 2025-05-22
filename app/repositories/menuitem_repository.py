from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from app.infrastructure.db.orm_models import MenuItem

class MenuItemRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> Optional[MenuItem]:
        stmt = select(MenuItem).where(MenuItem.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_nombre(self, value) -> Optional[MenuItem]:
        stmt = select(MenuItem).where(MenuItem.nombre == value)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> List[MenuItem]:
        stmt = select(MenuItem)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create(self, obj: MenuItem) -> MenuItem:
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, obj: MenuItem) -> None:
        await self.db.delete(obj)
        await self.db.commit()