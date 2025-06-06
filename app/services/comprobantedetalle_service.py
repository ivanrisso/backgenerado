# ✅ app/services/comprobantedetalle_service.py

from typing import List
from app.use_cases.comprobantedetalle_use_case import ComprobanteDetalleUseCase
from app.schemas.comprobante_detalle import ComprobanteDetalleCreate, ComprobanteDetalleUpdate, ComprobanteDetalleResponse
from app.domain.entities.comprobantedetalle import ComprobanteDetalle
from app.domain.exceptions.comprobantedetalle import ComprobanteDetalleNoEncontrado, ComprobanteDetalleDuplicado, ComprobanteDetalleInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class ComprobanteDetalleService:
    def __init__(self, use_case: ComprobanteDetalleUseCase):
        self.use_case = use_case

    def to_response(self, comprobantedetalle: ComprobanteDetalle) -> ComprobanteDetalleResponse:
        return ComprobanteDetalleResponse(**comprobantedetalle.__dict__)

    async def get_by_id(self, id: int) -> ComprobanteDetalleResponse:
        try:
            comprobantedetalle = await self.use_case.get_by_id(id)
            return self.to_response(comprobantedetalle)
        except ComprobanteDetalleNoEncontrado as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al obtener comprobantedetalle")

    async def get_all(self) -> List[ComprobanteDetalleResponse]:
        try:
            comprobantedetalles = await self.use_case.get_all()
            return [self.to_response(c) for c in comprobantedetalles]
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al listar comprobantedetalles")

    async def create(self, data: ComprobanteDetalleCreate) -> ComprobanteDetalleResponse:
        try:
            comprobantedetalle = await self.use_case.create(data)
            return self.to_response(comprobantedetalle)
        except (ComprobanteDetalleDuplicado, ClaveForaneaInvalida, ComprobanteDetalleInvalido) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear comprobantedetalle")

    async def update(self, id: int, data: ComprobanteDetalleUpdate) -> ComprobanteDetalleResponse:
        try:
            comprobantedetalle = await self.use_case.update(id, data)
            return self.to_response(comprobantedetalle)
        except (ComprobanteDetalleNoEncontrado, ComprobanteDetalleDuplicado, ClaveForaneaInvalida, ComprobanteDetalleInvalido) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al actualizar comprobantedetalle")

    async def delete(self, id: int) -> None:
        try:
            await self.use_case.delete(id)
        except (ComprobanteDetalleNoEncontrado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar comprobantedetalle")
