from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.use_cases.localidad_use_case import LocalidadUseCase
from app.schemas.localidad import LocalidadCreate
from app.infrastructure.db.orm_models import Localidad

class LocalidadService:
    def __init__(self, db: AsyncSession):
        self.use_case = LocalidadUseCase(db)

    async def get_by_id(self, id: int) -> Optional[Localidad]:
        return await self.use_case.get_by_id(id)

    async def list_all(self) -> List[Localidad]:
        return await self.use_case.list_all()

    async def create(self, data: LocalidadCreate) -> Localidad:
        return await self.use_case.create(data)