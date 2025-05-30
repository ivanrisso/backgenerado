from typing import  List
from app.domain.entities.moneda import Moneda
from app.domain.repository.moneda_repository_interfase import MonedaRepositoryInterface
from app.schemas.moneda import MonedaCreate, MonedaUpdate
from app.domain.exceptions.moneda import MonedaNoEncontrado
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class MonedaUseCase:
    def __init__(self, repo: MonedaRepositoryInterface):
        self.repo = repo

    async def get_by_id(self, moneda_id: int) -> Moneda:
        moneda = await self.repo.get_by_id(moneda_id)
        if not moneda:
            raise MonedaNoEncontrado(moneda_id)
        return moneda

    async def get_all(self) -> List[Moneda]:
        return await self.repo.get_all()

    async def create(self, data: MonedaCreate) -> Moneda:
        moneda = Moneda(id=None, **data.model_dump())
        return await self.repo.create(moneda)

    async def update(self, moneda_id: int, data: MonedaUpdate) -> Moneda:
        existing = await self.repo.get_by_id(moneda_id)
        if not existing:
            raise MonedaNoEncontrado(moneda_id)
        
        moneda = Moneda(id=moneda_id, **data.model_dump(exclude_unset=True))        
        return await self.repo.update(moneda_id, moneda)

    async def delete(self, moneda_id: int) -> None:
        existing = await self.repo.get_by_id(moneda_id)
        if not existing:
            raise MonedaNoEncontrado(moneda_id)

        await self.repo.delete(moneda_id)
