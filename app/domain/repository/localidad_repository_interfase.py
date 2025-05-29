# ✅ app/domain/repository/localidad_repository_interface.py
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.localidad import Localidad

class LocalidadRepositoryInterface(ABC):

    @abstractmethod
    async def get_by_id(self, localidad_id: int) -> Optional[Localidad]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Localidad]:
        pass

    @abstractmethod
    async def create(self, localidad: Localidad) -> Localidad:
        pass

    @abstractmethod
    async def update(self, localidad_id: int, localidad: Localidad) -> Localidad:
        pass

    @abstractmethod
    async def delete(self, localidad_id: int) -> None:
        pass
