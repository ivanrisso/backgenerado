from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from app.infrastructure.db.orm_models import Comprobante

class ComprobanteRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> Optional[Comprobante]:
        stmt = select(Comprobante).where(Comprobante.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_cliente_id(self, value) -> Optional[Comprobante]:
        stmt = select(Comprobante).where(Comprobante.cliente_id == value)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> List[Comprobante]:
        stmt = select(Comprobante)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create(self, obj: Comprobante) -> Comprobante:
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, obj: Comprobante) -> None:
        await self.db.delete(obj)
        await self.db.commit()