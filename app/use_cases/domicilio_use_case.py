from typing import  List
from app.domain.entities.domicilio import Domicilio
from app.domain.repository.domicilio_repository_interfase import DomicilioRepositoryInterface
from app.schemas.domicilio import DomicilioCreate, DomicilioUpdate
from app.domain.exceptions.domicilio import DomicilioNoEncontrado
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class DomicilioUseCase:
    def __init__(self, repo: DomicilioRepositoryInterface):
        self.repo = repo

    async def get_by_id(self, domicilio_id: int) -> Domicilio:
        domicilio = await self.repo.get_by_id(domicilio_id)
        if not domicilio:
            raise DomicilioNoEncontrado(domicilio_id)
        return domicilio

    async def get_all(self) -> List[Domicilio]:
        return await self.repo.get_all()

    async def create(self, data: DomicilioCreate) -> Domicilio:
        domicilio = Domicilio(id=None, **data.model_dump())
        return await self.repo.create(domicilio)

    async def update(self, domicilio_id: int, data: DomicilioUpdate) -> Domicilio:
        existing = await self.repo.get_by_id(domicilio_id)
        if not existing:
            raise DomicilioNoEncontrado(domicilio_id)
        
        domicilio = Domicilio(id=domicilio_id, **data.model_dump(exclude_unset=True))        
        return await self.repo.update(domicilio_id, domicilio)

    async def delete(self, domicilio_id: int) -> None:
        existing = await self.repo.get_by_id(domicilio_id)
        if not existing:
            raise DomicilioNoEncontrado(domicilio_id)

        await self.repo.delete(domicilio_id)
