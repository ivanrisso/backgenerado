from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.orm_models import Cliente
from app.repositories.cliente_repository import ClienteRepository
from app.schemas.cliente import ClienteCreate

class ClienteUseCase:
    def __init__(self, db: AsyncSession):
        self.repo = ClienteRepository(db)

    async def get_by_id(self, id: int) -> Optional[Cliente]:
        return await self.repo.get_by_id(id)

    async def list_all(self) -> List[Cliente]:
        return await self.repo.list_all()

    async def create(self, data: ClienteCreate) -> Cliente:
        obj = Cliente(**data.model_dump())
        return await self.repo.create(obj)