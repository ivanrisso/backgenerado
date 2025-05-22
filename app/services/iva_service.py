from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.use_cases.iva_use_case import IvaUseCase
from app.schemas.iva import IvaCreate
from app.infrastructure.db.orm_models import Iva

class IvaService:
    def __init__(self, db: AsyncSession):
        self.use_case = IvaUseCase(db)

    async def get_by_id(self, id: int) -> Optional[Iva]:
        return await self.use_case.get_by_id(id)

    async def list_all(self) -> List[Iva]:
        return await self.use_case.list_all()

    async def create(self, data: IvaCreate) -> Iva:
        return await self.use_case.create(data)