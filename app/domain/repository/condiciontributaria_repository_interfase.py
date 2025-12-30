from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.condiciontributaria import CondicionTributaria

class CondicionTributariaRepositoryInterface(ABC):

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[CondicionTributaria]:
        pass

    @abstractmethod
    async def get_all(self) -> List[CondicionTributaria]:
        pass

    @abstractmethod
    async def create(self, condicion: CondicionTributaria) -> CondicionTributaria:
        pass

    @abstractmethod
    async def update(self, id: int, condicion: CondicionTributaria) -> CondicionTributaria:
        pass

    @abstractmethod
    async def delete(self, id: int) -> None:
        pass
