from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.use_cases.usuario_use_case import UsuarioUseCase
from app.schemas.usuario import UsuarioCreate
from app.domain.usuario import Usuario

class UsuarioService:
    def __init__(self, db: AsyncSession):
        self.use_case = UsuarioUseCase(db)

    async def get_by_id(self, id: int) -> Optional[Usuario]:
        return await self.use_case.get_by_id(id)

    async def list_all(self) -> List[Usuario]:
        return await self.use_case.list_all()

    async def create(self, data: UsuarioCreate) -> Usuario:
        return await self.use_case.create(data)