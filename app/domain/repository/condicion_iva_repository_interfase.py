from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.condicion_iva import CondicionIva

class CondicionIvaRepositoryInterface(ABC):
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[CondicionIva]:
        pass

    @abstractmethod
    async def get_all(self) -> List[CondicionIva]:
        pass

    @abstractmethod
    async def create(self, entity: CondicionIva) -> CondicionIva:
        pass

    @abstractmethod
    async def update(self, id: int, entity: CondicionIva) -> Optional[CondicionIva]:
        pass

    @abstractmethod
    async def delete(self, id: int) -> None:
        pass
