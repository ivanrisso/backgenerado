# ✅ app/domain/repository/tipotel_repository_interface.py
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.tipotel import TipoTel

class TipoTelRepositoryInterface(ABC):

    @abstractmethod
    async def get_by_id(self, tipotel_id: int) -> Optional[TipoTel]:
        pass

    @abstractmethod
    async def get_all(self) -> List[TipoTel]:
        pass

    @abstractmethod
    async def create(self, tipotel: TipoTel) -> TipoTel:
        pass

    @abstractmethod
    async def update(self, tipotel_id: int, tipotel: TipoTel) -> TipoTel:
        pass

    @abstractmethod
    async def delete(self, tipotel_id: int) -> None:
        pass
