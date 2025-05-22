from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.orm_models import Localidad
from app.repositories.localidad_repository import LocalidadRepository
from app.schemas.localidad import LocalidadCreate

class LocalidadUseCase:
    def __init__(self, db: AsyncSession):
        self.repo = LocalidadRepository(db)

    async def get_by_id(self, id: int) -> Optional[Localidad]:
        return await self.repo.get_by_id(id)

    async def list_all(self) -> List[Localidad]:
        return await self.repo.list_all()

    async def create(self, data: LocalidadCreate) -> Localidad:
        obj = Localidad(**data.model_dump())
        return await self.repo.create(obj)