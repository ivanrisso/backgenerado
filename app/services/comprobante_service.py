# ✅ app/services/comprobante_service.py

from typing import List
from app.use_cases.comprobante_use_case import ComprobanteUseCase
from app.schemas.comprobante import ComprobanteCreate, ComprobanteUpdate, ComprobanteResponse
from app.domain.entities.comprobante import Comprobante
from app.domain.exceptions.comprobante import ComprobanteNoEncontrado, ComprobanteDuplicado, ComprobanteInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class ComprobanteService:
    def __init__(self, use_case: ComprobanteUseCase):
        self.use_case = use_case

    def to_response(self, comprobante: Comprobante) -> ComprobanteResponse:
        return ComprobanteResponse(**comprobante.__dict__)

    async def get_by_id(self, id: int) -> ComprobanteResponse:
        try:
            comprobante = await self.use_case.get_by_id(id)
            return self.to_response(comprobante)
        except ComprobanteNoEncontrado as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al obtener comprobante")

    async def get_all(self) -> List[ComprobanteResponse]:
        try:
            comprobantes = await self.use_case.get_all()
            return [self.to_response(c) for c in comprobantes]
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al listar comprobantes")

    async def create(self, data: ComprobanteCreate) -> ComprobanteResponse:
        try:
            comprobante = await self.use_case.create(data)
            return self.to_response(comprobante)
        except (ComprobanteDuplicado, ClaveForaneaInvalida, ComprobanteInvalido) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear comprobante")

    async def update(self, id: int, data: ComprobanteUpdate) -> ComprobanteResponse:
        try:
            comprobante = await self.use_case.update(id, data)
            return self.to_response(comprobante)
        except (ComprobanteNoEncontrado, ComprobanteDuplicado, ClaveForaneaInvalida, ComprobanteInvalido) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al actualizar comprobante")

    async def delete(self, id: int) -> None:
        try:
            await self.use_case.delete(id)
        except (ComprobanteNoEncontrado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar comprobante")
