from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from app.infrastructure.db.orm_models import CuentaCorriente

class CuentaCorrienteRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> Optional[CuentaCorriente]:
        stmt = select(CuentaCorriente).where(CuentaCorriente.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_cliente_id(self, value) -> Optional[CuentaCorriente]:
        stmt = select(CuentaCorriente).where(CuentaCorriente.cliente_id == value)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> List[CuentaCorriente]:
        stmt = select(CuentaCorriente)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create(self, obj: CuentaCorriente) -> CuentaCorriente:
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, obj: CuentaCorriente) -> None:
        await self.db.delete(obj)
        await self.db.commit()