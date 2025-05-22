from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.orm_models import Rol
from app.repositories.rol_repository import RolRepository
from app.schemas.rol import RolCreate

class RolUseCase:
    def __init__(self, db: AsyncSession):
        self.repo = RolRepository(db)

    async def get_by_id(self, id: int) -> Optional[Rol]:
        return await self.repo.get_by_id(id)

    async def list_all(self) -> List[Rol]:
        return await self.repo.list_all()

    async def create(self, data: RolCreate) -> Rol:
        obj = Rol(**data.model_dump())
        return await self.repo.create(obj)