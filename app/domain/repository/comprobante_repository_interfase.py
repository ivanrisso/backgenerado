# ✅ app/domain/repository/comprobante_repository_interface.py
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.comprobante import Comprobante

class ComprobanteRepositoryInterface(ABC):

    @abstractmethod
    async def get_by_id(self, comprobante_id: int) -> Optional[Comprobante]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Comprobante]:
        pass

    @abstractmethod
    async def create(self, comprobante: Comprobante) -> Comprobante:
        pass

    @abstractmethod
    async def update(self, comprobante_id: int, comprobante: Comprobante) -> Comprobante:
        pass

    @abstractmethod
    async def delete(self, comprobante_id: int) -> None:
        pass
