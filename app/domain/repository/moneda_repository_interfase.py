# ✅ app/domain/repository/moneda_repository_interface.py
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.moneda import Moneda

class MonedaRepositoryInterface(ABC):

    @abstractmethod
    async def get_by_id(self, moneda_id: int) -> Optional[Moneda]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Moneda]:
        pass

    @abstractmethod
    async def create(self, moneda: Moneda) -> Moneda:
        pass

    @abstractmethod
    async def update(self, moneda_id: int, moneda: Moneda) -> Moneda:
        pass

    @abstractmethod
    async def delete(self, moneda_id: int) -> None:
        pass
