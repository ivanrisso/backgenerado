from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.orm_models import Provincia
from app.repositories.provincia_repository import ProvinciaRepository
from app.domain.provincia import Provincia
from app.schemas.provincia import ProvinciaCreate

class ProvinciaUseCase:
    def __init__(self, db: AsyncSession):
        self.repo = ProvinciaRepository(db)

    async def get_by_id(self, id: int) -> Optional[Provincia]:
        return await self.repo.get_by_id(id)

    async def list_all(self) -> List[Provincia]:
        return await self.repo.list_all()

    async def create(self, data: ProvinciaCreate) -> Provincia:
        obj = Provincia(**data.model_dump())
        return await self.repo.create(obj)