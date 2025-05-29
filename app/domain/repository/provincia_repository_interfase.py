# ✅ app/domain/repository/provincia_repository_interface.py
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.provincia import Provincia

class ProvinciaRepositoryInterface(ABC):

    @abstractmethod
    async def get_by_id(self, provincia_id: int) -> Optional[Provincia]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Provincia]:
        pass

    @abstractmethod
    async def create(self, provincia: Provincia) -> Provincia:
        pass

    @abstractmethod
    async def update(self, provincia_id: int, provincia: Provincia) -> Provincia:
        pass

    @abstractmethod
    async def delete(self, provincia_id: int) -> None:
        pass
