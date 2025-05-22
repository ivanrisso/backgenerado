from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from app.infrastructure.db.orm_models import Cliente

class ClienteRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> Optional[Cliente]:
        stmt = select(Cliente).where(Cliente.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_nombre(self, value) -> Optional[Cliente]:
        stmt = select(Cliente).where(Cliente.nombre == value)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> List[Cliente]:
        stmt = select(Cliente)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create(self, obj: Cliente) -> Cliente:
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, obj: Cliente) -> None:
        await self.db.delete(obj)
        await self.db.commit()