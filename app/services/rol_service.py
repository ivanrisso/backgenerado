# ✅ app/services/rol_service.py

from typing import List
from app.use_cases.rol_use_case import RolUseCase
from app.schemas.rol import RolCreate, RolUpdate, RolResponse
from app.domain.entities.rol import Rol
from app.domain.exceptions.rol import RolNoEncontrado, RolDuplicado, RolInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class RolService:
    def __init__(self, use_case: RolUseCase):
        self.use_case = use_case

    def to_response(self, rol: Rol) -> RolResponse:
        return RolResponse(**rol.__dict__)

    async def get_by_id(self, id: int) -> RolResponse:
        try:
            rol = await self.use_case.get_by_id(id)
            return self.to_response(rol)
        except RolNoEncontrado as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al obtener rol")

    async def get_all(self) -> List[RolResponse]:
        try:
            rols = await self.use_case.get_all()
            return [self.to_response(c) for c in rols]
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al listar rols")

    async def create(self, data: RolCreate) -> RolResponse:
        try:
            rol = await self.use_case.create(data)
            return self.to_response(rol)
        except (RolDuplicado, ClaveForaneaInvalida, RolInvalido) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear rol")

    async def update(self, id: int, data: RolUpdate) -> RolResponse:
        try:
            rol = await self.use_case.update(id, data)
            return self.to_response(rol)
        except (RolNoEncontrado, RolDuplicado, ClaveForaneaInvalida, RolInvalido) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al actualizar rol")

    async def delete(self, id: int) -> None:
        try:
            await self.use_case.delete(id)
        except (RolNoEncontrado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar rol")
