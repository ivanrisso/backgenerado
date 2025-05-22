from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from app.infrastructure.db.orm_models import Domicilio

class DomicilioRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> Optional[Domicilio]:
        stmt = select(Domicilio).where(Domicilio.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_calle(self, value) -> Optional[Domicilio]:
        stmt = select(Domicilio).where(Domicilio.calle == value)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> List[Domicilio]:
        stmt = select(Domicilio)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create(self, obj: Domicilio) -> Domicilio:
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, obj: Domicilio) -> None:
        await self.db.delete(obj)
        await self.db.commit()