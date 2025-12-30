# ✅ app/domain/repository/telefono_repository_interface.py
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.telefono import Telefono

class TelefonoRepositoryInterface(ABC):

    @abstractmethod
    async def get_by_id(self, telefono_id: int) -> Optional[Telefono]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Telefono]:
        pass

    @abstractmethod
    async def get_by_domicilio(self, domicilio_id: int) -> List[Telefono]:
        pass

    @abstractmethod
    async def create(self, telefono: Telefono) -> Telefono:
        pass

    @abstractmethod
    async def update(self, telefono_id: int, telefono: Telefono) -> Telefono:
        pass

    @abstractmethod
    async def delete(self, telefono_id: int) -> None:
        pass
