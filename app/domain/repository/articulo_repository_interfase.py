from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.articulo import Articulo

class ArticuloRepositoryInterface(ABC):
    @abstractmethod
    async def get_by_id(self, articulo_id: int) -> Optional[Articulo]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Articulo]:
        pass

    @abstractmethod
    async def create(self, articulo: Articulo) -> Articulo:
        pass

    @abstractmethod
    async def update(self, articulo_id: int, articulo: Articulo) -> Optional[Articulo]:
        pass

    @abstractmethod
    async def delete(self, articulo_id: int) -> bool:
        pass

    @abstractmethod
    async def get_by_codigo(self, codigo: str) -> Optional[Articulo]:
        pass
