from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from app.infrastructure.db.orm_models import Cliente as ClienteSQL
from app.domain.entities.cliente import Cliente as ClienteDomain
from app.domain.repository.cliente_repository_interfase import ClienteRepositoryInterface



class ClienteRepositoryImpl(ClienteRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> Optional[ClienteDomain]:
        stmt = select(ClienteSQL).where(ClienteSQL.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()


    async def get_by_nombre(self, value) -> Optional[ClienteDomain]:
        stmt = select(ClienteSQL).where(ClienteSQL.nombre == value)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()


    async def list_all(self) -> List[ClienteDomain]:
        stmt = select(ClienteSQL)
        result = await self.db.execute(stmt)
        return result.scalars().all()


    async def create(self, obj: ClienteDomain) -> ClienteDomain:
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj


    async def delete(self, obj: ClienteDomain) -> None:
        await self.db.delete(obj)
        await self.db.commit()

        
    async def update(self, obj: ClienteDomain) -> ClienteDomain:
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj
        