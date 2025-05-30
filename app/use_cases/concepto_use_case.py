from typing import  List
from app.domain.entities.concepto import Concepto
from app.domain.repository.concepto_repository_interfase import ConceptoRepositoryInterface
from app.schemas.concepto import ConceptoCreate, ConceptoUpdate
from app.domain.exceptions.concepto import ConceptoNoEncontrado
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class ConceptoUseCase:
    def __init__(self, repo: ConceptoRepositoryInterface):
        self.repo = repo

    async def get_by_id(self, concepto_id: int) -> Concepto:
        concepto = await self.repo.get_by_id(concepto_id)
        if not concepto:
            raise ConceptoNoEncontrado(concepto_id)
        return concepto

    async def get_all(self) -> List[Concepto]:
        return await self.repo.get_all()

    async def create(self, data: ConceptoCreate) -> Concepto:
        concepto = Concepto(id=None, **data.model_dump())
        return await self.repo.create(concepto)

    async def update(self, concepto_id: int, data: ConceptoUpdate) -> Concepto:
        existing = await self.repo.get_by_id(concepto_id)
        if not existing:
            raise ConceptoNoEncontrado(concepto_id)
        
        concepto = Concepto(id=concepto_id, **data.model_dump(exclude_unset=True))        
        return await self.repo.update(concepto_id, concepto)

    async def delete(self, concepto_id: int) -> None:
        existing = await self.repo.get_by_id(concepto_id)
        if not existing:
            raise ConceptoNoEncontrado(concepto_id)

        await self.repo.delete(concepto_id)
