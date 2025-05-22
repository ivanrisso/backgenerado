from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from app.infrastructure.db.orm_models import Pais

class PaisRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> Optional[Pais]:
        stmt = select(Pais).where(Pais.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_codigo(self, value) -> Optional[Pais]:
        stmt = select(Pais).where(Pais.codigo == value)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> List[Pais]:
        stmt = select(Pais)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create(self, obj: Pais) -> Pais:
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, obj: Pais) -> None:
        await self.db.delete(obj)
        await self.db.commit()