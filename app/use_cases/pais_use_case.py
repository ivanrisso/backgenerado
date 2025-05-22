from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.orm_models import Pais
from app.repositories.pais_repository import PaisRepository
from app.schemas.pais import PaisCreate

class PaisUseCase:
    def __init__(self, db: AsyncSession):
        self.repo = PaisRepository(db)

    async def get_by_id(self, id: int) -> Optional[Pais]:
        return await self.repo.get_by_id(id)

    async def list_all(self) -> List[Pais]:
        return await self.repo.list_all()

    async def create(self, data: PaisCreate) -> Pais:
        obj = Pais(**data.model_dump())
        return await self.repo.create(obj)