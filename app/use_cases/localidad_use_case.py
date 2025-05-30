from typing import  List
from app.domain.entities.localidad import Localidad
from app.domain.repository.localidad_repository_interfase import LocalidadRepositoryInterface
from app.schemas.localidad import LocalidadCreate, LocalidadUpdate
from app.domain.exceptions.localidad import LocalidadNoEncontrado
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class LocalidadUseCase:
    def __init__(self, repo: LocalidadRepositoryInterface):
        self.repo = repo

    async def get_by_id(self, localidad_id: int) -> Localidad:
        localidad = await self.repo.get_by_id(localidad_id)
        if not localidad:
            raise LocalidadNoEncontrado(localidad_id)
        return localidad

    async def get_all(self) -> List[Localidad]:
        return await self.repo.get_all()

    async def create(self, data: LocalidadCreate) -> Localidad:
        localidad = Localidad(id=None, **data.model_dump())
        return await self.repo.create(localidad)

    async def update(self, localidad_id: int, data: LocalidadUpdate) -> Localidad:
        existing = await self.repo.get_by_id(localidad_id)
        if not existing:
            raise LocalidadNoEncontrado(localidad_id)
        
        localidad = Localidad(id=localidad_id, **data.model_dump(exclude_unset=True))        
        return await self.repo.update(localidad_id, localidad)

    async def delete(self, localidad_id: int) -> None:
        existing = await self.repo.get_by_id(localidad_id)
        if not existing:
            raise LocalidadNoEncontrado(localidad_id)

        await self.repo.delete(localidad_id)
