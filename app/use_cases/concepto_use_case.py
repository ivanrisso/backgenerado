from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.orm_models import Concepto
from app.repositories.concepto_repository import ConceptoRepository
from app.schemas.concepto import ConceptoCreate

class ConceptoUseCase:
    def __init__(self, db: AsyncSession):
        self.repo = ConceptoRepository(db)

    async def get_by_id(self, id: int) -> Optional[Concepto]:
        return await self.repo.get_by_id(id)

    async def list_all(self) -> List[Concepto]:
        return await self.repo.list_all()

    async def create(self, data: ConceptoCreate) -> Concepto:
        obj = Concepto(**data.model_dump())
        return await self.repo.create(obj)