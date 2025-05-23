from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.cliente import Cliente

class ClienteRepositoryInterface(ABC):

    @abstractmethod
    def get_by_id(self, cliente_id: int) -> Cliente:
        pass

    @abstractmethod
    def get_all(self) -> List[Cliente]:
        pass

    @abstractmethod
    def create(self, cliente: Cliente) -> Cliente:
        pass

    @abstractmethod
    def update(self, cliente_id: int, cliente: Cliente) -> Cliente:
        """Actualiza un cliente existente"""
        pass

    @abstractmethod
    def delete(self, cliente_id: int) -> None:
        pass
