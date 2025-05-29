# ✅ app/domain/repository/tipodom_repository_interface.py
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.tipodom import TipoDom

class TipoDomRepositoryInterface(ABC):

    @abstractmethod
    async def get_by_id(self, tipodom_id: int) -> Optional[TipoDom]:
        pass

    @abstractmethod
    async def get_all(self) -> List[TipoDom]:
        pass

    @abstractmethod
    async def create(self, tipodom: TipoDom) -> TipoDom:
        pass

    @abstractmethod
    async def update(self, tipodom_id: int, tipodom: TipoDom) -> TipoDom:
        pass

    @abstractmethod
    async def delete(self, tipodom_id: int) -> None:
        pass
