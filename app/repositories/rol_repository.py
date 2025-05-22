from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from app.infrastructure.db.orm_models import Rol

class RolRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> Optional[Rol]:
        stmt = select(Rol).where(Rol.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_rol_nombre(self, value) -> Optional[Rol]:
        stmt = select(Rol).where(Rol.rol_nombre == value)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> List[Rol]:
        stmt = select(Rol)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create(self, obj: Rol) -> Rol:
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, obj: Rol) -> None:
        await self.db.delete(obj)
        await self.db.commit()