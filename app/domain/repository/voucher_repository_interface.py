from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.voucher import Voucher

class VoucherRepositoryInterface(ABC):
    
    @abstractmethod
    async def get_by_id(self, voucher_id: str) -> Optional[Voucher]:
        """Obtiene un voucher por su ID externo."""
        pass

    # Nota: mark_as_billed no es necesario en la interfaz si es Solo Lectura externo.
    # El estado "facturado" se verifica contra la BD local.
