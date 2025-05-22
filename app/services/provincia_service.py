from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.use_cases.provincia_use_case import ProvinciaUseCase
from app.schemas.provincia import ProvinciaCreate
from app.infrastructure.db.orm_models import Provincia

class ProvinciaService:
    def __init__(self, db: AsyncSession):
        self.use_case = ProvinciaUseCase(db)

    async def get_by_id(self, id: int) -> Optional[Provincia]:
        return await self.use_case.get_by_id(id)

    async def list_all(self) -> List[Provincia]:
        return await self.use_case.list_all()

    async def create(self, data: ProvinciaCreate) -> Provincia:
        return await self.use_case.create(data)