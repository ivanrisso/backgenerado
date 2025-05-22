from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from app.infrastructure.db.orm_models import TipoDoc

class TipoDocRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> Optional[TipoDoc]:
        stmt = select(TipoDoc).where(TipoDoc.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_tipo_doc_nombre(self, value) -> Optional[TipoDoc]:
        stmt = select(TipoDoc).where(TipoDoc.tipo_doc_nombre == value)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> List[TipoDoc]:
        stmt = select(TipoDoc)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create(self, obj: TipoDoc) -> TipoDoc:
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, obj: TipoDoc) -> None:
        await self.db.delete(obj)
        await self.db.commit()