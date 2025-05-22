from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.use_cases.rol_use_case import RolUseCase
from app.schemas.rol import RolCreate
from app.infrastructure.db.orm_models import Rol

class RolService:
    def __init__(self, db: AsyncSession):
        self.use_case = RolUseCase(db)

    async def get_by_id(self, id: int) -> Optional[Rol]:
        return await self.use_case.get_by_id(id)

    async def list_all(self) -> List[Rol]:
        return await self.use_case.list_all()

    async def create(self, data: RolCreate) -> Rol:
        return await self.use_case.create(data)