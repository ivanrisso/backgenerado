from typing import  List
from app.domain.entities.pais import Pais
from app.domain.repository.pais_repository_interfase import PaisRepositoryInterface
from app.schemas.pais import PaisCreate, PaisUpdate
from app.domain.exceptions.pais import PaisNoEncontrado
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class PaisUseCase:
    def __init__(self, repo: PaisRepositoryInterface):
        self.repo = repo

    async def get_by_id(self, pais_id: int) -> Pais:
        pais = await self.repo.get_by_id(pais_id)
        if not pais:
            raise PaisNoEncontrado(pais_id)
        return pais

    async def get_all(self) -> List[Pais]:
        return await self.repo.get_all()

    async def create(self, data: PaisCreate) -> Pais:
        pais = Pais(id=None, **data.model_dump())
        return await self.repo.create(pais)

    async def update(self, pais_id: int, data: PaisUpdate) -> Pais:
        existing = await self.repo.get_by_id(pais_id)
        if not existing:
            raise PaisNoEncontrado(pais_id)
        
        pais = Pais(id=pais_id, **data.model_dump(exclude_unset=True))        
        return await self.repo.update(pais_id, pais)

    async def delete(self, pais_id: int) -> None:
        existing = await self.repo.get_by_id(pais_id)
        if not existing:
            raise PaisNoEncontrado(pais_id)

        await self.repo.delete(pais_id)
