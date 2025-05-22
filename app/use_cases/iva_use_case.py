from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.orm_models import Iva
from app.repositories.iva_repository import IvaRepository
from app.domain.iva import Iva
from app.schemas.iva import IvaCreate

class IvaUseCase:
    def __init__(self, db: AsyncSession):
        self.repo = IvaRepository(db)

    async def get_by_id(self, id: int) -> Optional[Iva]:
        return await self.repo.get_by_id(id)

    async def list_all(self) -> List[Iva]:
        return await self.repo.list_all()

    async def create(self, data: IvaCreate) -> Iva:
        obj = Iva(**data.model_dump())
        return await self.repo.create(obj)