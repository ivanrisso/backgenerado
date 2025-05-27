from typing import Optional, List
from app.domain.entities.tipodoc import TipoDoc
from app.domain.repository.tipodoc_repository_interfase import TipoDocRepositoryInterface
from app.schemas.tipo_doc import TipoDocCreate, TipoDocUpdate
from app.domain.exceptions.tipodoc import TipoDocNoEncontrado
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class TipoDocUseCase:
    def __init__(self, repo: TipoDocRepositoryInterface):
        self.repo = repo

    async def get_by_id(self, tipodoc_id: int) -> TipoDoc:
        tipodoc = await self.repo.get_by_id(tipodoc_id)
        if not tipodoc:
            raise TipoDocNoEncontrado(tipodoc_id)
        return tipodoc

    async def get_all(self) -> List[TipoDoc]:
        return await self.repo.get_all()

    async def create(self, data: TipoDocCreate) -> TipoDoc:
        tipodoc = TipoDoc(id=None, **data.model_dump())
        return await self.repo.create(tipodoc)

    async def update(self, tipodoc_id: int, data: TipoDocUpdate) -> TipoDoc:
        existing = await self.repo.get_by_id(tipodoc_id)        
        if not existing:
            raise TipoDocNoEncontrado(tipodoc_id)
        
        tipodoc = TipoDoc(id=tipodoc_id, **data.model_dump(exclude_unset=True))   
        return await self.repo.update(tipodoc_id, tipodoc)

    async def delete(self, tipodoc_id: int) -> None:
        existing = await self.repo.get_by_id(tipodoc_id)
        if not existing:
            raise TipoDocNoEncontrado(tipodoc_id)

        await self.repo.delete(tipodoc_id)
