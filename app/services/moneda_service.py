# ✅ app/services/moneda_service.py

from typing import List
from app.use_cases.moneda_use_case import MonedaUseCase
from app.schemas.moneda import MonedaCreate, MonedaUpdate, MonedaResponse
from app.domain.entities.moneda import Moneda
from app.domain.exceptions.moneda import MonedaNoEncontrado, MonedaDuplicado
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class MonedaService:
    def __init__(self, use_case: MonedaUseCase):
        self.use_case = use_case

    def to_response(self, moneda: Moneda) -> MonedaResponse:
        return MonedaResponse(**moneda.__dict__)

    async def get_by_id(self, id: int) -> MonedaResponse:
        try:
            moneda = await self.use_case.get_by_id(id)
            return self.to_response(moneda)
        except MonedaNoEncontrado as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al obtener moneda")

    async def get_all(self) -> List[MonedaResponse]:
        try:
            monedas = await self.use_case.get_all()
            return [self.to_response(c) for c in monedas]
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al listar monedas")

    async def create(self, data: MonedaCreate) -> MonedaResponse:
        try:
            moneda = await self.use_case.create(data)
            return self.to_response(moneda)
        except (MonedaDuplicado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear moneda")

    async def update(self, id: int, data: MonedaUpdate) -> MonedaResponse:
        try:
            moneda = await self.use_case.update(id, data)
            return self.to_response(moneda)
        except (MonedaNoEncontrado, MonedaDuplicado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al actualizar moneda")

    async def delete(self, id: int) -> None:
        try:
            await self.use_case.delete(id)
        except (MonedaNoEncontrado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar moneda")
