from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.entities.cliente import Cliente as ClienteDomain
from app.repositories.cliente_repository import ClienteRepositoryImpl
from app.schemas.cliente import ClienteCreate, ClienteUpdate

class ClienteUseCase:
    def __init__(self, db: AsyncSession):
        self.repo = ClienteRepositoryImpl(db)

    async def get_by_id(self, cliente_id: int) -> Optional[ClienteDomain]:
        return await self.repo.get_by_id(cliente_id)

    async def get_all(self) -> List[ClienteDomain]:
        return await self.repo.get_all()

    async def create(self, data: ClienteCreate) -> ClienteDomain:
        cliente = ClienteDomain(**data.model_dump())
        return await self.repo.create(cliente)

    async def update(self, cliente_id: int, data: ClienteUpdate) -> ClienteDomain:
        cliente = ClienteDomain(id=cliente_id, **data.model_dump())
        return await self.repo.update(cliente_id, cliente)

    async def delete(self, cliente_id: int) -> None:
        await self.repo.delete(cliente_id)
