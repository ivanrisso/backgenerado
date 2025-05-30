from typing import  List
from app.domain.entities.rolesusuario import RolesUsuario
from app.domain.repository.rolesusuario_repository_interfase import RolesUsuarioRepositoryInterface
from app.schemas.rolesusuario import RolesUsuarioCreate, RolesUsuarioUpdate
from app.domain.exceptions.rolesusuario import RolesUsuarioNoEncontrado
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class RolesUsuarioUseCase:
    def __init__(self, repo: RolesUsuarioRepositoryInterface):
        self.repo = repo

    async def get_by_id(self, rolesusuario_id: int) -> RolesUsuario:
        rolesusuario = await self.repo.get_by_id(rolesusuario_id)
        if not rolesusuario:
            raise RolesUsuarioNoEncontrado(rolesusuario_id)
        return rolesusuario

    async def get_all(self) -> List[RolesUsuario]:
        return await self.repo.get_all()

    async def create(self, data: RolesUsuarioCreate) -> RolesUsuario:
        rolesusuario = RolesUsuario(id=None, **data.model_dump())
        return await self.repo.create(rolesusuario)

    async def update(self, rolesusuario_id: int, data: RolesUsuarioUpdate) -> RolesUsuario:
        existing = await self.repo.get_by_id(rolesusuario_id)
        if not existing:
            raise RolesUsuarioNoEncontrado(rolesusuario_id)
        
        rolesusuario = RolesUsuario(id=rolesusuario_id, **data.model_dump(exclude_unset=True))        
        return await self.repo.update(rolesusuario_id, rolesusuario)

    async def delete(self, rolesusuario_id: int) -> None:
        existing = await self.repo.get_by_id(rolesusuario_id)
        if not existing:
            raise RolesUsuarioNoEncontrado(rolesusuario_id)

        await self.repo.delete(rolesusuario_id)
