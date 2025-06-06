# ✅ app/services/tipodom_service.py

from typing import List
from app.use_cases.tipodom_use_case import TipoDomUseCase
from app.schemas.tipodom import TipoDomCreate, TipoDomUpdate, TipoDomResponse
from app.domain.entities.tipodom import TipoDom
from app.domain.exceptions.tipodom import TipoDomNoEncontrado, TipoDomDuplicado, TipoDomInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class TipoDomService:
    def __init__(self, use_case: TipoDomUseCase):
        self.use_case = use_case

    def to_response(self, tipodom: TipoDom) -> TipoDomResponse:
        return TipoDomResponse(**tipodom.__dict__)

    async def get_by_id(self, id: int) -> TipoDomResponse:
        try:
            tipodom = await self.use_case.get_by_id(id)
            return self.to_response(tipodom)
        except TipoDomNoEncontrado as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al obtener tipodom")

    async def get_all(self) -> List[TipoDomResponse]:
        try:
            tipodoms = await self.use_case.get_all()
            return [self.to_response(c) for c in tipodoms]
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al listar tipodoms")

    async def create(self, data: TipoDomCreate) -> TipoDomResponse:
        try:
            tipodom = await self.use_case.create(data)
            return self.to_response(tipodom)
        except (TipoDomDuplicado, ClaveForaneaInvalida, TipoDomInvalido) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear tipodom")

    async def update(self, id: int, data: TipoDomUpdate) -> TipoDomResponse:
        try:
            tipodom = await self.use_case.update(id, data)
            return self.to_response(tipodom)
        except (TipoDomNoEncontrado, TipoDomDuplicado, ClaveForaneaInvalida, TipoDomInvalido) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al actualizar tipodom")

    async def delete(self, id: int) -> None:
        try:
            await self.use_case.delete(id)
        except (TipoDomNoEncontrado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar tipodom")
