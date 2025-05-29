# ✅ app/domain/repository/tipoimpuesto_repository_interface.py
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.tipoimpuesto import TipoImpuesto

class TipoImpuestoRepositoryInterface(ABC):

    @abstractmethod
    async def get_by_id(self, tipoimpuesto_id: int) -> Optional[TipoImpuesto]:
        pass

    @abstractmethod
    async def get_all(self) -> List[TipoImpuesto]:
        pass

    @abstractmethod
    async def create(self, tipoimpuesto: TipoImpuesto) -> TipoImpuesto:
        pass

    @abstractmethod
    async def update(self, tipoimpuesto_id: int, tipoimpuesto: TipoImpuesto) -> TipoImpuesto:
        pass

    @abstractmethod
    async def delete(self, tipoimpuesto_id: int) -> None:
        pass
