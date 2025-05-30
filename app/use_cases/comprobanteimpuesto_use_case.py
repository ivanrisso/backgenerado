from typing import  List
from app.domain.entities.comprobanteimpuesto import ComprobanteImpuesto
from app.domain.repository.comprobanteimpuesto_repository_interfase import ComprobanteImpuestoRepositoryInterface
from app.schemas.comprobante_impuesto import ComprobanteImpuestoCreate, ComprobanteImpuestoUpdate
from app.domain.exceptions.comprobanteimpuesto import ComprobanteImpuestoNoEncontrado
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class ComprobanteImpuestoUseCase:
    def __init__(self, repo: ComprobanteImpuestoRepositoryInterface):
        self.repo = repo

    async def get_by_id(self, comprobanteimpuesto_id: int) -> ComprobanteImpuesto:
        comprobanteimpuesto = await self.repo.get_by_id(comprobanteimpuesto_id)
        if not comprobanteimpuesto:
            raise ComprobanteImpuestoNoEncontrado(comprobanteimpuesto_id)
        return comprobanteimpuesto

    async def get_all(self) -> List[ComprobanteImpuesto]:
        return await self.repo.get_all()

    async def create(self, data: ComprobanteImpuestoCreate) -> ComprobanteImpuesto:
        comprobanteimpuesto = ComprobanteImpuesto(id=None, **data.model_dump())
        return await self.repo.create(comprobanteimpuesto)

    async def update(self, comprobanteimpuesto_id: int, data: ComprobanteImpuestoUpdate) -> ComprobanteImpuesto:
        existing = await self.repo.get_by_id(comprobanteimpuesto_id)
        if not existing:
            raise ComprobanteImpuestoNoEncontrado(comprobanteimpuesto_id)
        
        comprobanteimpuesto = ComprobanteImpuesto(id=comprobanteimpuesto_id, **data.model_dump(exclude_unset=True))        
        return await self.repo.update(comprobanteimpuesto_id, comprobanteimpuesto)

    async def delete(self, comprobanteimpuesto_id: int) -> None:
        existing = await self.repo.get_by_id(comprobanteimpuesto_id)
        if not existing:
            raise ComprobanteImpuestoNoEncontrado(comprobanteimpuesto_id)

        await self.repo.delete(comprobanteimpuesto_id)
