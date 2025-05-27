# ✅ app/domain/repository/iva_repository_interface.py
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.iva import Iva

class IvaRepositoryInterface(ABC):

    @abstractmethod
    async def get_by_id(self, iva_id: int) -> Optional[Iva]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Iva]:
        pass

    @abstractmethod
    async def create(self, iva: Iva) -> Iva:
        pass

    @abstractmethod
    async def update(self, iva_id: int, iva: Iva) -> Iva:
        pass

    @abstractmethod
    async def delete(self, iva_id: int) -> None:
        pass
