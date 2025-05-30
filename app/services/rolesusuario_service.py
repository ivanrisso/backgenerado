# ✅ app/services/rolesusuario_service.py

from typing import List
from app.use_cases.rolesusuario_use_case import RolesUsuarioUseCase
from app.schemas.rolesusuario import RolesUsuarioCreate, RolesUsuarioUpdate, RolesUsuarioResponse
from app.domain.entities.rolesusuario import RolesUsuario
from app.domain.exceptions.rolesusuario import RolesUsuarioNoEncontrado, RolesUsuarioDuplicado
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class RolesUsuarioService:
    def __init__(self, use_case: RolesUsuarioUseCase):
        self.use_case = use_case

    def to_response(self, rolesusuario: RolesUsuario) -> RolesUsuarioResponse:
        return RolesUsuarioResponse(**rolesusuario.__dict__)

    async def get_by_id(self, id: int) -> RolesUsuarioResponse:
        try:
            rolesusuario = await self.use_case.get_by_id(id)
            return self.to_response(rolesusuario)
        except RolesUsuarioNoEncontrado as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al obtener rolesusuario")

    async def get_all(self) -> List[RolesUsuarioResponse]:
        try:
            rolesusuarios = await self.use_case.get_all()
            return [self.to_response(c) for c in rolesusuarios]
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al listar rolesusuarios")

    async def create(self, data: RolesUsuarioCreate) -> RolesUsuarioResponse:
        try:
            rolesusuario = await self.use_case.create(data)
            return self.to_response(rolesusuario)
        except (RolesUsuarioDuplicado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear rolesusuario")

    async def update(self, id: int, data: RolesUsuarioUpdate) -> RolesUsuarioResponse:
        try:
            rolesusuario = await self.use_case.update(id, data)
            return self.to_response(rolesusuario)
        except (RolesUsuarioNoEncontrado, RolesUsuarioDuplicado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al actualizar rolesusuario")

    async def delete(self, id: int) -> None:
        try:
            await self.use_case.delete(id)
        except (RolesUsuarioNoEncontrado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar rolesusuario")
