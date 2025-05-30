from typing import  List
from app.domain.entities.comprobantedetalle import ComprobanteDetalle
from app.domain.repository.comprobantedetalle_repository_interfase import ComprobanteDetalleRepositoryInterface
from app.schemas.comprobante_detalle import ComprobanteDetalleCreate, ComprobanteDetalleUpdate
from app.domain.exceptions.comprobantedetalle import ComprobanteDetalleNoEncontrado
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class ComprobanteDetalleUseCase:
    def __init__(self, repo: ComprobanteDetalleRepositoryInterface):
        self.repo = repo

    async def get_by_id(self, comprobantedetalle_id: int) -> ComprobanteDetalle:
        comprobantedetalle = await self.repo.get_by_id(comprobantedetalle_id)
        if not comprobantedetalle:
            raise ComprobanteDetalleNoEncontrado(comprobantedetalle_id)
        return comprobantedetalle

    async def get_all(self) -> List[ComprobanteDetalle]:
        return await self.repo.get_all()

    async def create(self, data: ComprobanteDetalleCreate) -> ComprobanteDetalle:
        comprobantedetalle = ComprobanteDetalle(id=None, **data.model_dump())
        return await self.repo.create(comprobantedetalle)

    async def update(self, comprobantedetalle_id: int, data: ComprobanteDetalleUpdate) -> ComprobanteDetalle:
        existing = await self.repo.get_by_id(comprobantedetalle_id)
        if not existing:
            raise ComprobanteDetalleNoEncontrado(comprobantedetalle_id)
        
        comprobantedetalle = ComprobanteDetalle(id=comprobantedetalle_id, **data.model_dump(exclude_unset=True))        
        return await self.repo.update(comprobantedetalle_id, comprobantedetalle)

    async def delete(self, comprobantedetalle_id: int) -> None:
        existing = await self.repo.get_by_id(comprobantedetalle_id)
        if not existing:
            raise ComprobanteDetalleNoEncontrado(comprobantedetalle_id)

        await self.repo.delete(comprobantedetalle_id)
