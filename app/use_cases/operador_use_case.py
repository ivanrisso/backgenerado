from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.orm_models import Operador
from app.repositories.operador_repository import OperadorRepository
from app.schemas.operador import OperadorCreate

class OperadorUseCase:
    def __init__(self, db: AsyncSession):
        self.repo = OperadorRepository(db)

    async def get_by_id(self, id: int) -> Optional[Operador]:
        return await self.repo.get_by_id(id)

    async def list_all(self) -> List[Operador]:
        return await self.repo.list_all()

    async def create(self, data: OperadorCreate) -> Operador:
        obj = Operador(**data.model_dump())
        return await self.repo.create(obj)