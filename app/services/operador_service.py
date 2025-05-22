from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.use_cases.operador_use_case import OperadorUseCase
from app.schemas.operador import OperadorCreate
from app.infrastructure.db.orm_models import Operador

class OperadorService:
    def __init__(self, db: AsyncSession):
        self.use_case = OperadorUseCase(db)

    async def get_by_id(self, id: int) -> Optional[Operador]:
        return await self.use_case.get_by_id(id)

    async def list_all(self) -> List[Operador]:
        return await self.use_case.list_all()

    async def create(self, data: OperadorCreate) -> Operador:
        return await self.use_case.create(data)