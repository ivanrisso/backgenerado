from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.use_cases.telefono_use_case import TelefonoUseCase
from app.schemas.telefono import TelefonoCreate
from app.domain.telefono import Telefono

class TelefonoService:
    def __init__(self, db: AsyncSession):
        self.use_case = TelefonoUseCase(db)

    async def get_by_id(self, id: int) -> Optional[Telefono]:
        return await self.use_case.get_by_id(id)

    async def list_all(self) -> List[Telefono]:
        return await self.use_case.list_all()

    async def create(self, data: TelefonoCreate) -> Telefono:
        return await self.use_case.create(data)