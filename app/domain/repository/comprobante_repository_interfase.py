# ✅ app/domain/repository/comprobante_repository_interface.py
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date
from app.domain.entities.comprobante import Comprobante

class ComprobanteRepositoryInterface(ABC):

    @abstractmethod
    async def get_by_id(self, comprobante_id: int) -> Optional[Comprobante]:
        pass

    @abstractmethod
    async def get_by_voucher_id(self, voucher_id: str) -> Optional[Comprobante]:
        pass

    @abstractmethod
    async def get_all(
        self, 
        tipo_comprobante_id: Optional[int] = None,
        cliente_id: Optional[int] = None,
        fecha_desde: Optional[date] = None,
        fecha_hasta: Optional[date] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Comprobante]:
        pass

    @abstractmethod
    async def get_last_number(self, tipo_comprobante_id: int, punto_venta: int) -> int:
        """Obtiene el último número de comprobante para un tipo y punto de venta."""
        pass
        
    @abstractmethod
    async def create(self, comprobante: Comprobante, commit: bool = True) -> Comprobante:
        pass

    @abstractmethod
    async def update(self, comprobante_id: int, comprobante: Comprobante) -> Comprobante:
        pass

    @abstractmethod
    async def delete(self, comprobante_id: int) -> None:
        pass
