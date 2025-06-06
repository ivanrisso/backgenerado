# ✅ app/services/localidad_service.py

from typing import List
from app.use_cases.localidad_use_case import LocalidadUseCase
from app.schemas.localidad import LocalidadCreate, LocalidadUpdate, LocalidadResponse
from app.domain.entities.localidad import Localidad
from app.domain.exceptions.localidad import LocalidadNoEncontrado, LocalidadDuplicado, LocalidadInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class LocalidadService:
    def __init__(self, use_case: LocalidadUseCase):
        self.use_case = use_case

    def to_response(self, localidad: Localidad) -> LocalidadResponse:
        return LocalidadResponse(**localidad.__dict__)

    async def get_by_id(self, id: int) -> LocalidadResponse:
        try:
            localidad = await self.use_case.get_by_id(id)
            return self.to_response(localidad)
        except LocalidadNoEncontrado as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al obtener localidad")

    async def get_all(self) -> List[LocalidadResponse]:
        try:
            localidads = await self.use_case.get_all()
            return [self.to_response(c) for c in localidads]
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al listar localidads")

    async def create(self, data: LocalidadCreate) -> LocalidadResponse:
        try:
            localidad = await self.use_case.create(data)
            return self.to_response(localidad)
        except (LocalidadDuplicado, ClaveForaneaInvalida, LocalidadInvalido) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear localidad")

    async def update(self, id: int, data: LocalidadUpdate) -> LocalidadResponse:
        try:
            localidad = await self.use_case.update(id, data)
            return self.to_response(localidad)
        except (LocalidadNoEncontrado, LocalidadDuplicado, ClaveForaneaInvalida, LocalidadInvalido) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al actualizar localidad")

    async def delete(self, id: int) -> None:
        try:
            await self.use_case.delete(id)
        except (LocalidadNoEncontrado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar localidad")
