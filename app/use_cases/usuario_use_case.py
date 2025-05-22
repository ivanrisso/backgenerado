from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.orm_models import Usuario
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.usuario import UsuarioCreate

class UsuarioUseCase:
    def __init__(self, db: AsyncSession):
        self.repo = UsuarioRepository(db)

    async def get_by_id(self, id: int) -> Optional[Usuario]:
        return await self.repo.get_by_id(id)

    async def list_all(self) -> List[Usuario]:
        return await self.repo.list_all()

    async def create(self, data: UsuarioCreate) -> Usuario:
        obj = Usuario(**data.model_dump())
        return await self.repo.create(obj)