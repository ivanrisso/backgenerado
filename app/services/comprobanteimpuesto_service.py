# ✅ app/services/comprobanteimpuesto_service.py

from typing import List
from app.use_cases.comprobanteimpuesto_use_case import ComprobanteImpuestoUseCase
from app.schemas.comprobante_impuesto import ComprobanteImpuestoCreate, ComprobanteImpuestoUpdate, ComprobanteImpuestoResponse
from app.domain.entities.comprobanteimpuesto import ComprobanteImpuesto
from app.domain.exceptions.comprobanteimpuesto import ComprobanteImpuestoNoEncontrado, ComprobanteImpuestoDuplicado
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class ComprobanteImpuestoService:
    def __init__(self, use_case: ComprobanteImpuestoUseCase):
        self.use_case = use_case

    def to_response(self, comprobanteimpuesto: ComprobanteImpuesto) -> ComprobanteImpuestoResponse:
        return ComprobanteImpuestoResponse(**comprobanteimpuesto.__dict__)

    async def get_by_id(self, id: int) -> ComprobanteImpuestoResponse:
        try:
            comprobanteimpuesto = await self.use_case.get_by_id(id)
            return self.to_response(comprobanteimpuesto)
        except ComprobanteImpuestoNoEncontrado as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al obtener comprobanteimpuesto")

    async def get_all(self) -> List[ComprobanteImpuestoResponse]:
        try:
            comprobanteimpuestos = await self.use_case.get_all()
            return [self.to_response(c) for c in comprobanteimpuestos]
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al listar comprobanteimpuestos")

    async def create(self, data: ComprobanteImpuestoCreate) -> ComprobanteImpuestoResponse:
        try:
            comprobanteimpuesto = await self.use_case.create(data)
            return self.to_response(comprobanteimpuesto)
        except (ComprobanteImpuestoDuplicado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear comprobanteimpuesto")

    async def update(self, id: int, data: ComprobanteImpuestoUpdate) -> ComprobanteImpuestoResponse:
        try:
            comprobanteimpuesto = await self.use_case.update(id, data)
            return self.to_response(comprobanteimpuesto)
        except (ComprobanteImpuestoNoEncontrado, ComprobanteImpuestoDuplicado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al actualizar comprobanteimpuesto")

    async def delete(self, id: int) -> None:
        try:
            await self.use_case.delete(id)
        except (ComprobanteImpuestoNoEncontrado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar comprobanteimpuesto")
