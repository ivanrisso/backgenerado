# ✅ app/services/provincia_service.py

from typing import List
from app.use_cases.provincia_use_case import ProvinciaUseCase
from app.schemas.provincia import ProvinciaCreate, ProvinciaUpdate, ProvinciaResponse
from app.domain.entities.provincia import Provincia
from app.domain.exceptions.provincia import ProvinciaNoEncontrado, ProvinciaDuplicado, ProvinciaInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class ProvinciaService:
    def __init__(self, use_case: ProvinciaUseCase):
        self.use_case = use_case

    def to_response(self, provincia: Provincia) -> ProvinciaResponse:
        return ProvinciaResponse(**provincia.__dict__)

    async def get_by_id(self, id: int) -> ProvinciaResponse:
        try:
            provincia = await self.use_case.get_by_id(id)
            return self.to_response(provincia)
        except ProvinciaNoEncontrado as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al obtener provincia")

    async def get_all(self) -> List[ProvinciaResponse]:
        try:
            provincias = await self.use_case.get_all()
            return [self.to_response(c) for c in provincias]
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al listar provincias")

    async def create(self, data: ProvinciaCreate) -> ProvinciaResponse:
        try:
            provincia = await self.use_case.create(data)
            return self.to_response(provincia)
        except (ProvinciaDuplicado, ClaveForaneaInvalida, ProvinciaInvalido) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear provincia")

    async def update(self, id: int, data: ProvinciaUpdate) -> ProvinciaResponse:
        try:
            provincia = await self.use_case.update(id, data)
            return self.to_response(provincia)
        except (ProvinciaNoEncontrado, ProvinciaDuplicado, ClaveForaneaInvalida, ProvinciaInvalido) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al actualizar provincia")

    async def delete(self, id: int) -> None:
        try:
            await self.use_case.delete(id)
        except (ProvinciaNoEncontrado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar provincia")
