# ✅ app/domain/repository/comprobanteimpuesto_repository_interface.py
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.comprobanteimpuesto import ComprobanteImpuesto

class ComprobanteImpuestoRepositoryInterface(ABC):

    @abstractmethod
    async def get_by_id(self, comprobanteimpuesto_id: int) -> Optional[ComprobanteImpuesto]:
        pass

    @abstractmethod
    async def get_all(self) -> List[ComprobanteImpuesto]:
        pass

    @abstractmethod
    async def create(self, comprobanteimpuesto: ComprobanteImpuesto) -> ComprobanteImpuesto:
        pass

    @abstractmethod
    async def update(self, comprobanteimpuesto_id: int, comprobanteimpuesto: ComprobanteImpuesto) -> ComprobanteImpuesto:
        pass

    @abstractmethod
    async def delete(self, comprobanteimpuesto_id: int) -> None:
        pass
