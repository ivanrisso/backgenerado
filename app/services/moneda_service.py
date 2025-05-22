from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.use_cases.moneda_use_case import MonedaUseCase
from app.schemas.moneda import MonedaCreate
from app.infrastructure.db.orm_models import Moneda

class MonedaService:
    def __init__(self, db: AsyncSession):
        self.use_case = MonedaUseCase(db)

    async def get_by_id(self, id: int) -> Optional[Moneda]:
        return await self.use_case.get_by_id(id)

    async def list_all(self) -> List[Moneda]:
        return await self.use_case.list_all()

    async def create(self, data: MonedaCreate) -> Moneda:
        return await self.use_case.create(data)