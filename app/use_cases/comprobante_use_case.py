from typing import  List
from app.domain.entities.comprobante import Comprobante
from app.domain.repository.comprobante_repository_interfase import ComprobanteRepositoryInterface
from app.schemas.comprobante import ComprobanteCreate, ComprobanteUpdate
from app.domain.exceptions.comprobante import ComprobanteNoEncontrado
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class ComprobanteUseCase:
    def __init__(self, repo: ComprobanteRepositoryInterface):
        self.repo = repo

    async def get_by_id(self, comprobante_id: int) -> Comprobante:
        comprobante = await self.repo.get_by_id(comprobante_id)
        if not comprobante:
            raise ComprobanteNoEncontrado(comprobante_id)
        return comprobante

    async def get_all(self) -> List[Comprobante]:
        return await self.repo.get_all()

    async def create(self, data: ComprobanteCreate) -> Comprobante:
        
        comprobante = Comprobante(id=None, **data.model_dump())                            
        return await self.repo.create(comprobante)

    async def update(self, comprobante_id: int, data: ComprobanteUpdate) -> Comprobante:
        existing = await self.repo.get_by_id(comprobante_id)
        if not existing:
            raise ComprobanteNoEncontrado(comprobante_id)
        
        comprobante = Comprobante(id=comprobante_id, **data.model_dump(exclude_unset=True))        
        return await self.repo.update(comprobante_id, comprobante)

    async def delete(self, comprobante_id: int) -> None:
        existing = await self.repo.get_by_id(comprobante_id)
        if not existing:
            raise ComprobanteNoEncontrado(comprobante_id)

        await self.repo.delete(comprobante_id)
