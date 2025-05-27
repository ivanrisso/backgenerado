# ✅ app/domain/repository/usuario_repository_interface.py
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.usuario import Usuario

class UsuarioRepositoryInterface(ABC):

    @abstractmethod
    async def get_by_id(self, usuario_id: int) -> Optional[Usuario]:
        pass

    @abstractmethod
    async def get_by_email(self, usuario_mail: int) -> Optional[Usuario]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Usuario]:
        pass

    @abstractmethod
    async def create(self, usuario: Usuario) -> Usuario:
        pass

    @abstractmethod
    async def update(self, usuario_id: int, usuario: Usuario) -> Usuario:
        pass

    @abstractmethod
    async def delete(self, usuario_id: int) -> None:
        pass
