# ✅ app/domain/repository/cliente_repository_interface.py
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.cliente import Cliente

class ClienteRepositoryInterface(ABC):

    @abstractmethod
    async def get_by_id(self, cliente_id: int) -> Optional[Cliente]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Cliente]:
        pass

    @abstractmethod
    async def create(self, cliente: Cliente) -> Cliente:
        pass

    @abstractmethod
    async def update(self, cliente_id: int, cliente: Cliente) -> Cliente:
        pass

    @abstractmethod
    async def delete(self, cliente_id: int) -> None:
        pass
