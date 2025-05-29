# ✅ app/domain/repository/comprobantedetalle_repository_interface.py
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.comprobantedetalle import ComprobanteDetalle

class ComprobanteDetalleRepositoryInterface(ABC):

    @abstractmethod
    async def get_by_id(self, comprobantedetalle_id: int) -> Optional[ComprobanteDetalle]:
        pass

    @abstractmethod
    async def get_all(self) -> List[ComprobanteDetalle]:
        pass

    @abstractmethod
    async def create(self, comprobantedetalle: ComprobanteDetalle) -> ComprobanteDetalle:
        pass

    @abstractmethod
    async def update(self, comprobantedetalle_id: int, comprobantedetalle: ComprobanteDetalle) -> ComprobanteDetalle:
        pass

    @abstractmethod
    async def delete(self, comprobantedetalle_id: int) -> None:
        pass
