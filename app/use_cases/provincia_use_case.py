from typing import  List
from app.domain.entities.provincia import Provincia
from app.domain.repository.provincia_repository_interfase import ProvinciaRepositoryInterface
from app.schemas.provincia import ProvinciaCreate, ProvinciaUpdate
from app.domain.exceptions.provincia import ProvinciaNoEncontrado
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class ProvinciaUseCase:
    def __init__(self, repo: ProvinciaRepositoryInterface):
        self.repo = repo

    async def get_by_id(self, provincia_id: int) -> Provincia:
        provincia = await self.repo.get_by_id(provincia_id)
        if not provincia:
            raise ProvinciaNoEncontrado(provincia_id)
        return provincia

    async def get_all(self) -> List[Provincia]:
        return await self.repo.get_all()

    async def create(self, data: ProvinciaCreate) -> Provincia:
        provincia = Provincia(id=None, **data.model_dump())
        return await self.repo.create(provincia)

    async def update(self, provincia_id: int, data: ProvinciaUpdate) -> Provincia:
        existing = await self.repo.get_by_id(provincia_id)
        if not existing:
            raise ProvinciaNoEncontrado(provincia_id)
        
        provincia = Provincia(id=provincia_id, **data.model_dump(exclude_unset=True))        
        return await self.repo.update(provincia_id, provincia)

    async def delete(self, provincia_id: int) -> None:
        existing = await self.repo.get_by_id(provincia_id)
        if not existing:
            raise ProvinciaNoEncontrado(provincia_id)

        await self.repo.delete(provincia_id)
