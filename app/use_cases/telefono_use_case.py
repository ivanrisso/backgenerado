from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.orm_models import Telefono
from app.repositories.telefono_repository import TelefonoRepository
from app.schemas.telefono import TelefonoCreate

class TelefonoUseCase:
    def __init__(self, db: AsyncSession):
        self.repo = TelefonoRepository(db)

    async def get_by_id(self, id: int) -> Optional[Telefono]:
        return await self.repo.get_by_id(id)

    async def list_all(self) -> List[Telefono]:
        return await self.repo.list_all()

    async def create(self, data: TelefonoCreate) -> Telefono:
        obj = Telefono(**data.model_dump())
        return await self.repo.create(obj)