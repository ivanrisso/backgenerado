from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from app.infrastructure.db.orm_models import ComprobanteImpuesto

class ComprobanteImpuestoRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> Optional[ComprobanteImpuesto]:
        stmt = select(ComprobanteImpuesto).where(ComprobanteImpuesto.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_comprobante_id(self, value) -> Optional[ComprobanteImpuesto]:
        stmt = select(ComprobanteImpuesto).where(ComprobanteImpuesto.comprobante_id == value)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> List[ComprobanteImpuesto]:
        stmt = select(ComprobanteImpuesto)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create(self, obj: ComprobanteImpuesto) -> ComprobanteImpuesto:
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, obj: ComprobanteImpuesto) -> None:
        await self.db.delete(obj)
        await self.db.commit()