# ✅ app/domain/repository/tipocomprobante_repository_interface.py
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.tipocomprobante import TipoComprobante

class TipoComprobanteRepositoryInterface(ABC):

    @abstractmethod
    async def get_by_id(self, tipocomprobante_id: int) -> Optional[TipoComprobante]:
        pass

    @abstractmethod
    async def get_all(self) -> List[TipoComprobante]:
        pass

    @abstractmethod
    async def create(self, tipocomprobante: TipoComprobante) -> TipoComprobante:
        pass

    @abstractmethod
    async def update(self, tipocomprobante_id: int, tipocomprobante: TipoComprobante) -> TipoComprobante:
        pass

    @abstractmethod
    async def delete(self, tipocomprobante_id: int) -> None:
        pass
