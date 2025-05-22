from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.orm_models import Domicilio
from app.repositories.domicilio_repository import DomicilioRepository
from app.schemas.domicilio import DomicilioCreate

class DomicilioUseCase:
    def __init__(self, db: AsyncSession):
        self.repo = DomicilioRepository(db)

    async def get_by_id(self, id: int) -> Optional[Domicilio]:
        return await self.repo.get_by_id(id)

    async def list_all(self) -> List[Domicilio]:
        return await self.repo.list_all()

    async def create(self, data: DomicilioCreate) -> Domicilio:
        obj = Domicilio(**data.model_dump())
        return await self.repo.create(obj)