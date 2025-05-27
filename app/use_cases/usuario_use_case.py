from typing import Optional, List
from app.domain.entities.usuario import Usuario
from app.domain.repository.usuario_repository_interfase import UsuarioRepositoryInterface
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.domain.exceptions.usuario import UsuarioNoEncontrado
from app.infrastructure.security.password_hashing import hash_password

class UsuarioUseCase:
    def __init__(self, repo: UsuarioRepositoryInterface):
        self.repo = repo

    async def get_by_id(self, usuario_id: int) -> Usuario:
        usuario = await self.repo.get_by_id(usuario_id)
        if not usuario:
            raise UsuarioNoEncontrado(usuario_id)
        return usuario

    async def get_by_email(self, usuario_mail: int) -> Usuario:
        usuario = await self.repo.get_by_email(usuario_mail)
        if not usuario:
            raise UsuarioNoEncontrado(usuario_mail)
        return usuario

    async def get_all(self) -> List[Usuario]:
        return await self.repo.get_all()

    async def create(self, data: UsuarioCreate) -> Usuario:
        usuario = Usuario(id=None, **data.model_dump())
        
        usuario = Usuario(
            usuario_email=data.usuario_email,
            usuario_password=hash_password(data.usuario_password),
            nombre=data.nombre,
            apellido=data.apellido,
        )
        
        return await self.repo.create(usuario)

    async def update(self, usuario_id: int, data: UsuarioUpdate) -> Usuario:
        existing = await self.repo.get_by_id(usuario_id)
        if not existing:
            raise UsuarioNoEncontrado(usuario_id)
        
        usuario = Usuario(id=usuario_id, **data.model_dump(exclude_unset=True))        
        return await self.repo.update(usuario_id, usuario)

    async def delete(self, usuario_id: int) -> None:
        existing = await self.repo.get_by_id(usuario_id)
        if not existing:
            raise UsuarioNoEncontrado(usuario_id)

        await self.repo.delete(usuario_id)
