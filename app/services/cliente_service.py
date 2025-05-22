from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.use_cases.cliente_use_case import ClienteUseCase
from app.schemas.cliente import ClienteCreate
from app.infrastructure.db.orm_models import Cliente 


class ClienteService:
    def __init__(self, db: AsyncSession):
        self.use_case = ClienteUseCase(db)

    async def get_by_id(self, id: int) -> Optional[Cliente]:
        return await self.use_case.get_by_id(id)

    async def list_all(self) -> List[Cliente]:
        return await self.use_case.list_all()

    async def create(self, data: ClienteCreate) -> Cliente:
        return await self.use_case.create(data)