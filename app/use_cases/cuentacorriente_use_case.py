from typing import  List
from app.domain.entities.cuentacorriente import CuentaCorriente
from app.domain.repository.cuentacorriente_repository_interfase import CuentaCorrienteRepositoryInterface
from app.schemas.cuenta_corriente import CuentaCorrienteCreate, CuentaCorrienteUpdate
from app.domain.exceptions.cuentacorriente import CuentaCorrienteNoEncontrado
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class CuentaCorrienteUseCase:
    def __init__(self, repo: CuentaCorrienteRepositoryInterface):
        self.repo = repo

    async def get_by_id(self, cuentacorriente_id: int) -> CuentaCorriente:
        cuentacorriente = await self.repo.get_by_id(cuentacorriente_id)
        if not cuentacorriente:
            raise CuentaCorrienteNoEncontrado(cuentacorriente_id)
        return cuentacorriente

    async def get_all(self) -> List[CuentaCorriente]:
        return await self.repo.get_all()

    async def create(self, data: CuentaCorrienteCreate) -> CuentaCorriente:
        cuentacorriente = CuentaCorriente(id=None, **data.model_dump())
        return await self.repo.create(cuentacorriente)

    async def update(self, cuentacorriente_id: int, data: CuentaCorrienteUpdate) -> CuentaCorriente:
        existing = await self.repo.get_by_id(cuentacorriente_id)
        if not existing:
            raise CuentaCorrienteNoEncontrado(cuentacorriente_id)
        
        cuentacorriente = CuentaCorriente(id=cuentacorriente_id, **data.model_dump(exclude_unset=True))        
        return await self.repo.update(cuentacorriente_id, cuentacorriente)

    async def delete(self, cuentacorriente_id: int) -> None:
        existing = await self.repo.get_by_id(cuentacorriente_id)
        if not existing:
            raise CuentaCorrienteNoEncontrado(cuentacorriente_id)

        await self.repo.delete(cuentacorriente_id)
