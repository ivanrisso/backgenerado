from typing import  List
from app.domain.entities.tipodom import TipoDom
from app.domain.repository.tipodom_repository_interfase import TipoDomRepositoryInterface
from app.schemas.tipodom import TipoDomCreate, TipoDomUpdate
from app.domain.exceptions.tipodom import TipoDomNoEncontrado
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class TipoDomUseCase:
    def __init__(self, repo: TipoDomRepositoryInterface):
        self.repo = repo

    async def get_by_id(self, tipodom_id: int) -> TipoDom:
        tipodom = await self.repo.get_by_id(tipodom_id)
        if not tipodom:
            raise TipoDomNoEncontrado(tipodom_id)
        return tipodom

    async def get_all(self) -> List[TipoDom]:
        return await self.repo.get_all()

    async def create(self, data: TipoDomCreate) -> TipoDom:
        tipodom = TipoDom(id=None, **data.model_dump())
        return await self.repo.create(tipodom)

    async def update(self, tipodom_id: int, data: TipoDomUpdate) -> TipoDom:
        existing = await self.repo.get_by_id(tipodom_id)
        if not existing:
            raise TipoDomNoEncontrado(tipodom_id)
        
        tipodom = TipoDom(id=tipodom_id, **data.model_dump(exclude_unset=True))        
        return await self.repo.update(tipodom_id, tipodom)

    async def delete(self, tipodom_id: int) -> None:
        existing = await self.repo.get_by_id(tipodom_id)
        if not existing:
            raise TipoDomNoEncontrado(tipodom_id)

        await self.repo.delete(tipodom_id)
