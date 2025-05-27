# ✅ app/domain/repository/tipodoc_repository_interface.py
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.tipodoc import TipoDoc

class TipoDocRepositoryInterface(ABC):

    @abstractmethod
    async def get_by_id(self, tipodoc_id: int) -> Optional[TipoDoc]:
        pass

    @abstractmethod
    async def get_all(self) -> List[TipoDoc]:
        pass

    @abstractmethod
    async def create(self, tipodoc: TipoDoc) -> TipoDoc:
        pass

    @abstractmethod
    async def update(self, tipodoc_id: int, tipodoc: TipoDoc) -> TipoDoc:
        pass

    @abstractmethod
    async def delete(self, tipodoc_id: int) -> None:
        pass
