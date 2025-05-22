from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.use_cases.rolesusuario_use_case import RolesUsuarioUseCase
from app.schemas.rolesusuario import RolesUsuarioCreate
from app.domain.rolesusuario import RolesUsuario

class RolesUsuarioService:
    def __init__(self, db: AsyncSession):
        self.use_case = RolesUsuarioUseCase(db)

    async def get_by_id(self, id: int) -> Optional[RolesUsuario]:
        return await self.use_case.get_by_id(id)

    async def list_all(self) -> List[RolesUsuario]:
        return await self.use_case.list_all()

    async def create(self, data: RolesUsuarioCreate) -> RolesUsuario:
        return await self.use_case.create(data)