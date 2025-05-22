from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.orm_models import TipoDom
from app.repositories.tipodom_repository import TipoDomRepository
from app.schemas.tipodom import TipoDomCreate

class TipoDomUseCase:
    def __init__(self, db: AsyncSession):
        self.repo = TipoDomRepository(db)

    async def get_by_id(self, id: int) -> Optional[TipoDom]:
        return await self.repo.get_by_id(id)

    async def list_all(self) -> List[TipoDom]:
        return await self.repo.list_all()

    async def create(self, data: TipoDomCreate) -> TipoDom:
        obj = TipoDom(**data.model_dump())
        return await self.repo.create(obj)