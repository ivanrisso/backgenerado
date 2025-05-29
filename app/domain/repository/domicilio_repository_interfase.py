# ✅ app/domain/repository/domicilio_repository_interface.py
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.domicilio import Domicilio

class DomicilioRepositoryInterface(ABC):

    @abstractmethod
    async def get_by_id(self, domicilio_id: int) -> Optional[Domicilio]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Domicilio]:
        pass

    @abstractmethod
    async def create(self, domicilio: Domicilio) -> Domicilio:
        pass

    @abstractmethod
    async def update(self, domicilio_id: int, domicilio: Domicilio) -> Domicilio:
        pass

    @abstractmethod
    async def delete(self, domicilio_id: int) -> None:
        pass
