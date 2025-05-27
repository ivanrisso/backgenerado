from typing import Optional, List
from app.domain.entities.iva import Iva
from app.domain.repository.iva_repository_interfase import IvaRepositoryInterface
from app.schemas.iva import IvaCreate, IvaUpdate
from app.domain.exceptions.iva import IvaNoEncontrado
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class IvaUseCase:
    def __init__(self, repo: IvaRepositoryInterface):
        self.repo = repo

    async def get_by_id(self, iva_id: int) -> Iva:
        iva = await self.repo.get_by_id(iva_id)
        if not iva:
            raise IvaNoEncontrado(iva_id)
        return iva

    async def get_all(self) -> List[Iva]:
        return await self.repo.get_all()

    async def create(self, data: IvaCreate) -> Iva:
        try:
            iva = Iva(id=None, **data.model_dump())
        except Exception as e:
            logger.exception(f"❌ Error instanciando Iva: {e}")
            raise
         
        return await self.repo.create(iva)

    async def update(self, iva_id: int, data: IvaUpdate) -> Iva:
        existing = await self.repo.get_by_id(iva_id)
        if not existing:
            raise IvaNoEncontrado(iva_id)
        
        iva = Iva(id=iva_id, **data.model_dump(exclude_unset=True))       
                 
        return await self.repo.update(iva_id, iva)

    async def delete(self, iva_id: int) -> None:
        existing = await self.repo.get_by_id(iva_id)
        if not existing:
            raise IvaNoEncontrado(iva_id)

        await self.repo.delete(iva_id)
