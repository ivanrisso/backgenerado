from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.use_cases.domicilio_use_case import DomicilioUseCase
from app.schemas.domicilio import DomicilioCreate
from app.domain.domicilio import Domicilio

class DomicilioService:
    def __init__(self, db: AsyncSession):
        self.use_case = DomicilioUseCase(db)

    async def get_by_id(self, id: int) -> Optional[Domicilio]:
        return await self.use_case.get_by_id(id)

    async def list_all(self) -> List[Domicilio]:
        return await self.use_case.list_all()

    async def create(self, data: DomicilioCreate) -> Domicilio:
        return await self.use_case.create(data)