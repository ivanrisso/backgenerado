from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.orm_models import Moneda
from app.repositories.moneda_repository import MonedaRepository
from app.domain.moneda import Moneda
from app.schemas.moneda import MonedaCreate

class MonedaUseCase:
    def __init__(self, db: AsyncSession):
        self.repo = MonedaRepository(db)

    async def get_by_id(self, id: int) -> Optional[Moneda]:
        return await self.repo.get_by_id(id)

    async def list_all(self) -> List[Moneda]:
        return await self.repo.list_all()

    async def create(self, data: MonedaCreate) -> Moneda:
        obj = Moneda(**data.model_dump())
        return await self.repo.create(obj)