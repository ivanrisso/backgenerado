# ✅ app/domain/repository/auditoriacomprobante_repository_interface.py
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.auditoriacomprobante import AuditoriaComprobante

class AuditoriaComprobanteRepositoryInterface(ABC):

    @abstractmethod
    async def get_by_id(self, auditoriacomprobante_id: int) -> Optional[AuditoriaComprobante]:
        pass

    @abstractmethod
    async def get_all(self) -> List[AuditoriaComprobante]:
        pass

    @abstractmethod
    async def create(self, auditoriacomprobante: AuditoriaComprobante) -> AuditoriaComprobante:
        pass

    @abstractmethod
    async def update(self, auditoriacomprobante_id: int, auditoriacomprobante: AuditoriaComprobante) -> AuditoriaComprobante:
        pass

    @abstractmethod
    async def delete(self, auditoriacomprobante_id: int) -> None:
        pass
