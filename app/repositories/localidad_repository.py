from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from app.infrastructure.db.orm_models import Localidad

class LocalidadRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> Optional[Localidad]:
        stmt = select(Localidad).where(Localidad.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_localidad_nombre(self, value) -> Optional[Localidad]:
        stmt = select(Localidad).where(Localidad.localidad_nombre == value)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> List[Localidad]:
        stmt = select(Localidad)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create(self, obj: Localidad) -> Localidad:
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, obj: Localidad) -> None:
        await self.db.delete(obj)
        await self.db.commit()