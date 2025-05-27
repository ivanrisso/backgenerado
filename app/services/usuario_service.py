# ✅ app/services/usuario_service.py

from typing import List
from app.use_cases.usuario_use_case import UsuarioUseCase
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from app.domain.entities.usuario import Usuario
from app.domain.exceptions.usuario import UsuarioNoEncontrado, UsuarioDuplicado
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida


class UsuarioService:
    def __init__(self, use_case: UsuarioUseCase):
        self.use_case = use_case

    def to_response(self, usuario: Usuario) -> UsuarioResponse:
        return UsuarioResponse(**usuario.__dict__)

    async def get_by_id(self, id: int) -> UsuarioResponse:
        try:
            usuario = await self.use_case.get_by_id(id)
            return self.to_response(usuario)
        except UsuarioNoEncontrado as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al obtener usuario")

    async def get_by_email(self, mail: str) -> UsuarioResponse:
        try:
            usuario = await self.use_case.get_by_email(mail)
            return self.to_response(usuario)
        except UsuarioNoEncontrado as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al obtener usuario")

    async def get_all(self) -> List[UsuarioResponse]:
        try:
            usuarios = await self.use_case.get_all()
            return [self.to_response(c) for c in usuarios]
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al listar usuarios")

    async def create(self, data: UsuarioCreate) -> UsuarioResponse:
        try:
            usuario = await self.use_case.create(data)
            return self.to_response(usuario)
        except (UsuarioDuplicado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear usuario")

    async def update(self, id: int, data: UsuarioUpdate) -> UsuarioResponse:
        try:
            usuario = await self.use_case.update(id, data)
            return self.to_response(usuario)
        except (UsuarioNoEncontrado, UsuarioDuplicado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al actualizar usuario")

    async def delete(self, id: int) -> None:
        try:
            await self.use_case.delete(id)
        except (UsuarioNoEncontrado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar usuario")
