from typing import Optional, List
from app.domain.entities.cliente import Cliente
from app.domain.repository.cliente_repository_interfase import ClienteRepositoryInterface
from app.schemas.cliente import ClienteCreate, ClienteUpdate
from app.domain.exceptions.cliente import ClienteNoEncontrado


class ClienteUseCase:
    def __init__(self, repo: ClienteRepositoryInterface):
        self.repo = repo

    async def get_by_id(self, cliente_id: int) -> Cliente:
        cliente = await self.repo.get_by_id(cliente_id)
        if not cliente:
            raise ClienteNoEncontrado(cliente_id)
        return cliente

    async def get_all(self) -> List[Cliente]:
        return await self.repo.get_all()

    async def create(self, data: ClienteCreate) -> Cliente:
        cliente = Cliente(id=None, **data.model_dump())
        return await self.repo.create(cliente)

    async def update(self, cliente_id: int, data: ClienteUpdate) -> Cliente:
        existing = await self.repo.get_by_id(cliente_id)
        if not existing:
            raise ClienteNoEncontrado(cliente_id)
        
        cliente = Cliente(id=cliente_id, **data.model_dump(exclude_unset=True))        
        return await self.repo.update(cliente_id, cliente)

    async def delete(self, cliente_id: int) -> None:
        existing = await self.repo.get_by_id(cliente_id)
        if not existing:
            raise ClienteNoEncontrado(cliente_id)

        await self.repo.delete(cliente_id)
