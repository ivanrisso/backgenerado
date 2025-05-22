from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from app.infrastructure.db.orm_models import TipoTel

class TipoTelRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> Optional[TipoTel]:
        stmt = select(TipoTel).where(TipoTel.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_nombre(self, value) -> Optional[TipoTel]:
        stmt = select(TipoTel).where(TipoTel.nombre == value)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> List[TipoTel]:
        stmt = select(TipoTel)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create(self, obj: TipoTel) -> TipoTel:
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, obj: TipoTel) -> None:
        await self.db.delete(obj)
        await self.db.commit()