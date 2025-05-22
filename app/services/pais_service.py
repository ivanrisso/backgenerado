from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.use_cases.pais_use_case import PaisUseCase
from app.schemas.pais import PaisCreate
from app.domain.pais import Pais

class PaisService:
    def __init__(self, db: AsyncSession):
        self.use_case = PaisUseCase(db)

    async def get_by_id(self, id: int) -> Optional[Pais]:
        return await self.use_case.get_by_id(id)

    async def list_all(self) -> List[Pais]:
        return await self.use_case.list_all()

    async def create(self, data: PaisCreate) -> Pais:
        return await self.use_case.create(data)