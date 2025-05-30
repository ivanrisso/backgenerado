from typing import  List
from app.domain.entities.auditoriacomprobante import AuditoriaComprobante
from app.domain.repository.auditoriacomprobante_repository_interfase import AuditoriaComprobanteRepositoryInterface
from app.schemas.auditoria_comprobante import AuditoriaComprobanteCreate, AuditoriaComprobanteUpdate
from app.domain.exceptions.auditoriacomprobante import AuditoriaComprobanteNoEncontrado
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class AuditoriaComprobanteUseCase:
    def __init__(self, repo: AuditoriaComprobanteRepositoryInterface):
        self.repo = repo

    async def get_by_id(self, auditoriacomprobante_id: int) -> AuditoriaComprobante:
        auditoriacomprobante = await self.repo.get_by_id(auditoriacomprobante_id)
        if not auditoriacomprobante:
            raise AuditoriaComprobanteNoEncontrado(auditoriacomprobante_id)
        return auditoriacomprobante

    async def get_all(self) -> List[AuditoriaComprobante]:
        return await self.repo.get_all()

    async def create(self, data: AuditoriaComprobanteCreate) -> AuditoriaComprobante:
        auditoriacomprobante = AuditoriaComprobante(id=None, **data.model_dump())
        return await self.repo.create(auditoriacomprobante)

    async def update(self, auditoriacomprobante_id: int, data: AuditoriaComprobanteUpdate) -> AuditoriaComprobante:
        existing = await self.repo.get_by_id(auditoriacomprobante_id)
        if not existing:
            raise AuditoriaComprobanteNoEncontrado(auditoriacomprobante_id)
        
        auditoriacomprobante = AuditoriaComprobante(id=auditoriacomprobante_id, **data.model_dump(exclude_unset=True))        
        return await self.repo.update(auditoriacomprobante_id, auditoriacomprobante)

    async def delete(self, auditoriacomprobante_id: int) -> None:
        existing = await self.repo.get_by_id(auditoriacomprobante_id)
        if not existing:
            raise AuditoriaComprobanteNoEncontrado(auditoriacomprobante_id)

        await self.repo.delete(auditoriacomprobante_id)
