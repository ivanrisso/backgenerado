from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from app.infrastructure.db.orm_models import Usuario

class UsuarioRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> Optional[Usuario]:
        stmt = select(Usuario).where(Usuario.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_usuario_email(self, value) -> Optional[Usuario]:
        stmt = select(Usuario).where(Usuario.usuario_email == value)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> List[Usuario]:
        stmt = select(Usuario)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create(self, obj: Usuario) -> Usuario:
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, obj: Usuario) -> None:
        await self.db.delete(obj)
        await self.db.commit()