# ✅ app/domain/repository/cuentacorriente_repository_interface.py
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.cuentacorriente import CuentaCorriente

class CuentaCorrienteRepositoryInterface(ABC):

    @abstractmethod
    async def get_by_id(self, cuentacorriente_id: int) -> Optional[CuentaCorriente]:
        pass

    @abstractmethod
    async def get_all(self) -> List[CuentaCorriente]:
        pass

    @abstractmethod
    async def create(self, cuentacorriente: CuentaCorriente, commit: bool = True) -> CuentaCorriente:
        pass

    @abstractmethod
    async def update(self, cuentacorriente_id: int, cuentacorriente: CuentaCorriente) -> CuentaCorriente:
        pass

    @abstractmethod
    async def delete(self, cuentacorriente_id: int) -> None:
        pass
