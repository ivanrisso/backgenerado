from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from app.infrastructure.db.orm_models import TipoDom

class TipoDomRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> Optional[TipoDom]:
        stmt = select(TipoDom).where(TipoDom.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_nombre(self, value) -> Optional[TipoDom]:
        stmt = select(TipoDom).where(TipoDom.nombre == value)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> List[TipoDom]:
        stmt = select(TipoDom)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create(self, obj: TipoDom) -> TipoDom:
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, obj: TipoDom) -> None:
        await self.db.delete(obj)
        await self.db.commit()