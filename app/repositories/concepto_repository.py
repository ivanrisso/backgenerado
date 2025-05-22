from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from app.infrastructure.db.orm_models import Concepto

class ConceptoRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> Optional[Concepto]:
        stmt = select(Concepto).where(Concepto.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_codigo(self, value) -> Optional[Concepto]:
        stmt = select(Concepto).where(Concepto.codigo == value)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> List[Concepto]:
        stmt = select(Concepto)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create(self, obj: Concepto) -> Concepto:
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, obj: Concepto) -> None:
        await self.db.delete(obj)
        await self.db.commit()