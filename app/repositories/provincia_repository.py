from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from app.infrastructure.db.orm_models import Provincia

class ProvinciaRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> Optional[Provincia]:
        stmt = select(Provincia).where(Provincia.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_provincia_nombre(self, value) -> Optional[Provincia]:
        stmt = select(Provincia).where(Provincia.provincia_nombre == value)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> List[Provincia]:
        stmt = select(Provincia)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create(self, obj: Provincia) -> Provincia:
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, obj: Provincia) -> None:
        await self.db.delete(obj)
        await self.db.commit()