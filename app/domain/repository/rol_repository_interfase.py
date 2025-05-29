# ✅ app/domain/repository/rol_repository_interface.py
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.rol import Rol

class RolRepositoryInterface(ABC):

    @abstractmethod
    async def get_by_id(self, rol_id: int) -> Optional[Rol]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Rol]:
        pass

    @abstractmethod
    async def create(self, rol: Rol) -> Rol:
        pass

    @abstractmethod
    async def update(self, rol_id: int, rol: Rol) -> Rol:
        pass

    @abstractmethod
    async def delete(self, rol_id: int) -> None:
        pass
