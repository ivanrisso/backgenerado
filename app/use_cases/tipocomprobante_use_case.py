from typing import  List
from app.domain.entities.tipocomprobante import TipoComprobante
from app.domain.repository.tipocomprobante_repository_interfase import TipoComprobanteRepositoryInterface
from app.schemas.tipocomprobante import TipoComprobanteCreate, TipoComprobanteUpdate
from app.domain.exceptions.tipocomprobante import TipoComprobanteNoEncontrado
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class TipoComprobanteUseCase:
    def __init__(self, repo: TipoComprobanteRepositoryInterface):
        self.repo = repo

    async def get_by_id(self, tipocomprobante_id: int) -> TipoComprobante:
        tipocomprobante = await self.repo.get_by_id(tipocomprobante_id)
        if not tipocomprobante:
            raise TipoComprobanteNoEncontrado(tipocomprobante_id)
        return tipocomprobante

    async def get_all(self) -> List[TipoComprobante]:
        return await self.repo.get_all()

    async def create(self, data: TipoComprobanteCreate) -> TipoComprobante:
        tipocomprobante = TipoComprobante(id=None, **data.model_dump())
        return await self.repo.create(tipocomprobante)

    async def update(self, tipocomprobante_id: int, data: TipoComprobanteUpdate) -> TipoComprobante:
        existing = await self.repo.get_by_id(tipocomprobante_id)
        if not existing:
            raise TipoComprobanteNoEncontrado(tipocomprobante_id)
        
        tipocomprobante = TipoComprobante(id=tipocomprobante_id, **data.model_dump(exclude_unset=True))        
        return await self.repo.update(tipocomprobante_id, tipocomprobante)

    async def delete(self, tipocomprobante_id: int) -> None:
        existing = await self.repo.get_by_id(tipocomprobante_id)
        if not existing:
            raise TipoComprobanteNoEncontrado(tipocomprobante_id)

        await self.repo.delete(tipocomprobante_id)
