from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from app.infrastructure.db.orm_models import Telefono

class TelefonoRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> Optional[Telefono]:
        stmt = select(Telefono).where(Telefono.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_tipo_tel_id(self, value) -> Optional[Telefono]:
        stmt = select(Telefono).where(Telefono.tipo_tel_id == value)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> List[Telefono]:
        stmt = select(Telefono)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create(self, obj: Telefono) -> Telefono:
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, obj: Telefono) -> None:
        await self.db.delete(obj)
        await self.db.commit()