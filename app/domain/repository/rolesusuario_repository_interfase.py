# ✅ app/domain/repository/rolesusuario_repository_interface.py
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.rolesusuario import RolesUsuario

class RolesUsuarioRepositoryInterface(ABC):

    @abstractmethod
    async def get_by_id(self, rolesusuario_id: int) -> Optional[RolesUsuario]:
        pass

    @abstractmethod
    async def get_all(self) -> List[RolesUsuario]:
        pass

    @abstractmethod
    async def create(self, rolesusuario: RolesUsuario) -> RolesUsuario:
        pass

    @abstractmethod
    async def update(self, rolesusuario_id: int, rolesusuario: RolesUsuario) -> RolesUsuario:
        pass

    @abstractmethod
    async def delete(self, rolesusuario_id: int) -> None:
        pass
