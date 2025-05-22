from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from app.infrastructure.db.orm_models import Moneda

class MonedaRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> Optional[Moneda]:
        stmt = select(Moneda).where(Moneda.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_codigo(self, value) -> Optional[Moneda]:
        stmt = select(Moneda).where(Moneda.codigo == value)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> List[Moneda]:
        stmt = select(Moneda)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create(self, obj: Moneda) -> Moneda:
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, obj: Moneda) -> None:
        await self.db.delete(obj)
        await self.db.commit()