from typing import  List
from app.domain.entities.rol import Rol
from app.domain.repository.rol_repository_interfase import RolRepositoryInterface
from app.schemas.rol import RolCreate, RolUpdate
from app.domain.exceptions.rol import RolNoEncontrado
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class RolUseCase:
    def __init__(self, repo: RolRepositoryInterface):
        self.repo = repo

    async def get_by_id(self, rol_id: int) -> Rol:
        rol = await self.repo.get_by_id(rol_id)
        if not rol:
            raise RolNoEncontrado(rol_id)
        return rol

    async def get_all(self) -> List[Rol]:
        return await self.repo.get_all()

    async def create(self, data: RolCreate) -> Rol:
        rol = Rol(id=None, **data.model_dump())
        return await self.repo.create(rol)

    async def update(self, rol_id: int, data: RolUpdate) -> Rol:
        existing = await self.repo.get_by_id(rol_id)
        if not existing:
            raise RolNoEncontrado(rol_id)
        
        rol = Rol(id=rol_id, **data.model_dump(exclude_unset=True))        
        return await self.repo.update(rol_id, rol)

    async def delete(self, rol_id: int) -> None:
        existing = await self.repo.get_by_id(rol_id)
        if not existing:
            raise RolNoEncontrado(rol_id)

        await self.repo.delete(rol_id)
