# ✅ app/domain/repository/clienteimpuesto_repository_interface.py
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.clienteimpuesto import ClienteImpuesto

class ClienteImpuestoRepositoryInterface(ABC):

    @abstractmethod
    async def get_by_id(self, clienteimpuesto_id: int) -> Optional[ClienteImpuesto]:
        pass

    @abstractmethod
    async def get_all(self) -> List[ClienteImpuesto]:
        pass

    @abstractmethod
    async def create(self, clienteimpuesto: ClienteImpuesto) -> ClienteImpuesto:
        pass

    @abstractmethod
    async def update(self, clienteimpuesto_id: int, clienteimpuesto: ClienteImpuesto) -> ClienteImpuesto:
        pass

    @abstractmethod
    async def delete(self, clienteimpuesto_id: int) -> None:
        pass
