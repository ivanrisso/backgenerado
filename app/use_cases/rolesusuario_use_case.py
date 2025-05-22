from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.orm_models import RolesUsuario
from app.repositories.rolesusuario_repository import RolesUsuarioRepository
from app.domain.rolesusuario import RolesUsuario
from app.schemas.rolesusuario import RolesUsuarioCreate

class RolesUsuarioUseCase:
    def __init__(self, db: AsyncSession):
        self.repo = RolesUsuarioRepository(db)

    async def get_by_id(self, id: int) -> Optional[RolesUsuario]:
        return await self.repo.get_by_id(id)

    async def list_all(self) -> List[RolesUsuario]:
        return await self.repo.list_all()

    async def create(self, data: RolesUsuarioCreate) -> RolesUsuario:
        obj = RolesUsuario(**data.model_dump())
        return await self.repo.create(obj)