from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.use_cases.tipodom_use_case import TipoDomUseCase
from app.schemas.tipodom import TipoDomCreate
from app.infrastructure.db.orm_models import TipoDom

class TipoDomService:
    def __init__(self, db: AsyncSession):
        self.use_case = TipoDomUseCase(db)

    async def get_by_id(self, id: int) -> Optional[TipoDom]:
        return await self.use_case.get_by_id(id)

    async def list_all(self) -> List[TipoDom]:
        return await self.use_case.list_all()

    async def create(self, data: TipoDomCreate) -> TipoDom:
        return await self.use_case.create(data)