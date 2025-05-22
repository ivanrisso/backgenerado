from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from app.infrastructure.db.orm_models import ComprobanteDetalle

class ComprobanteDetalleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> Optional[ComprobanteDetalle]:
        stmt = select(ComprobanteDetalle).where(ComprobanteDetalle.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_comprobante_id(self, value) -> Optional[ComprobanteDetalle]:
        stmt = select(ComprobanteDetalle).where(ComprobanteDetalle.comprobante_id == value)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> List[ComprobanteDetalle]:
        stmt = select(ComprobanteDetalle)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create(self, obj: ComprobanteDetalle) -> ComprobanteDetalle:
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, obj: ComprobanteDetalle) -> None:
        await self.db.delete(obj)
        await self.db.commit()