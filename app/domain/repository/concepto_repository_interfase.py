# ✅ app/domain/repository/concepto_repository_interface.py
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.concepto import Concepto

class ConceptoRepositoryInterface(ABC):

    @abstractmethod
    async def get_by_id(self, concepto_id: int) -> Optional[Concepto]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Concepto]:
        pass

    @abstractmethod
    async def create(self, concepto: Concepto) -> Concepto:
        pass

    @abstractmethod
    async def update(self, concepto_id: int, concepto: Concepto) -> Concepto:
        pass

    @abstractmethod
    async def delete(self, concepto_id: int) -> None:
        pass
