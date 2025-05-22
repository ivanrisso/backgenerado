from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.use_cases.concepto_use_case import ConceptoUseCase
from app.schemas.concepto import ConceptoCreate
from app.infrastructure.db.orm_models import Concepto

class ConceptoService:
    def __init__(self, db: AsyncSession):
        self.use_case = ConceptoUseCase(db)

    async def get_by_id(self, id: int) -> Optional[Concepto]:
        return await self.use_case.get_by_id(id)

    async def list_all(self) -> List[Concepto]:
        return await self.use_case.list_all()

    async def create(self, data: ConceptoCreate) -> Concepto:
        return await self.use_case.create(data)