# ✅ app/domain/repository/pais_repository_interface.py
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.pais import Pais

class PaisRepositoryInterface(ABC):

    @abstractmethod
    async def get_by_id(self, pais_id: int) -> Optional[Pais]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Pais]:
        pass

    @abstractmethod
    async def create(self, pais: Pais) -> Pais:
        pass

    @abstractmethod
    async def update(self, pais_id: int, pais: Pais) -> Pais:
        pass

    @abstractmethod
    async def delete(self, pais_id: int) -> None:
        pass
