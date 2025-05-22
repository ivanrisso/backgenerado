from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.infrastructure.db.orm_models import Iva as IvaModel
from app.domain.iva import Iva

class IvaRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> Iva:
        result = await self.db.execute(select(IvaModel).where(IvaModel.id == id))
        return result.scalar_one_or_none()

    async def get_by_codigo(self, value) -> Iva:
        result = await self.db.execute(select(IvaModel).where(IvaModel.codigo == value))
        return result.scalar_one_or_none()

    async def list_all(self) -> list[Iva]:
        result = await self.db.execute(select(IvaModel))
        return result.scalars().all()

    async def create(self, iva: Iva) -> Iva:
        db_obj = IvaModel(**iva.dict())
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj
        