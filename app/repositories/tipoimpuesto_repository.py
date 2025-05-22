from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from app.infrastructure.db.orm_models import TipoImpuesto

class TipoImpuestoRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> Optional[TipoImpuesto]:
        stmt = select(TipoImpuesto).where(TipoImpuesto.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_codigo_afip(self, value) -> Optional[TipoImpuesto]:
        stmt = select(TipoImpuesto).where(TipoImpuesto.codigo_afip == value)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> List[TipoImpuesto]:
        stmt = select(TipoImpuesto)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create(self, obj: TipoImpuesto) -> TipoImpuesto:
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, obj: TipoImpuesto) -> None:
        await self.db.delete(obj)
        await self.db.commit()