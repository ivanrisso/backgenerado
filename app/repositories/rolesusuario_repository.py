from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from app.infrastructure.db.orm_models import RolesUsuario

class RolesUsuarioRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> Optional[RolesUsuario]:
        stmt = select(RolesUsuario).where(RolesUsuario.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_usuario_id(self, value) -> Optional[RolesUsuario]:
        stmt = select(RolesUsuario).where(RolesUsuario.usuario_id == value)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> List[RolesUsuario]:
        stmt = select(RolesUsuario)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create(self, obj: RolesUsuario) -> RolesUsuario:
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, obj: RolesUsuario) -> None:
        await self.db.delete(obj)
        await self.db.commit()