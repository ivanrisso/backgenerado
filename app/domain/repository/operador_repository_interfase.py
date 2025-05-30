# ✅ app/domain/repository/operador_repository_interface.py
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.operador import Operador

class OperadorRepositoryInterface(ABC):

    @abstractmethod
    async def get_by_id(self, operador_id: int) -> Optional[Operador]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Operador]:
        pass

    @abstractmethod
    async def create(self, operador: Operador) -> Operador:
        pass

    @abstractmethod
    async def update(self, operador_id: int, operador: Operador) -> Operador:
        pass

    @abstractmethod
    async def delete(self, operador_id: int) -> None:
        pass
