from typing import  List
from app.domain.entities.clienteimpuesto import ClienteImpuesto
from app.domain.repository.clienteimpuesto_repository_interfase import ClienteImpuestoRepositoryInterface
from app.schemas.clienteimpuesto import ClienteImpuestoCreate, ClienteImpuestoUpdate
from app.domain.exceptions.clienteimpuesto import ClienteImpuestoNoEncontrado
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class ClienteImpuestoUseCase:
    def __init__(self, repo: ClienteImpuestoRepositoryInterface):
        self.repo = repo

    async def get_by_id(self, clienteimpuesto_id: int) -> ClienteImpuesto:
        clienteimpuesto = await self.repo.get_by_id(clienteimpuesto_id)
        if not clienteimpuesto:
            raise ClienteImpuestoNoEncontrado(clienteimpuesto_id)
        return clienteimpuesto

    async def get_all(self) -> List[ClienteImpuesto]:
        return await self.repo.get_all()

    async def create(self, data: ClienteImpuestoCreate) -> ClienteImpuesto:
        clienteimpuesto = ClienteImpuesto(id=None, **data.model_dump())
        return await self.repo.create(clienteimpuesto)

    async def update(self, clienteimpuesto_id: int, data: ClienteImpuestoUpdate) -> ClienteImpuesto:
        existing = await self.repo.get_by_id(clienteimpuesto_id)
        if not existing:
            raise ClienteImpuestoNoEncontrado(clienteimpuesto_id)
        
        clienteimpuesto = ClienteImpuesto(id=clienteimpuesto_id, **data.model_dump(exclude_unset=True))        
        return await self.repo.update(clienteimpuesto_id, clienteimpuesto)

    async def delete(self, clienteimpuesto_id: int) -> None:
        existing = await self.repo.get_by_id(clienteimpuesto_id)
        if not existing:
            raise ClienteImpuestoNoEncontrado(clienteimpuesto_id)

        await self.repo.delete(clienteimpuesto_id)
