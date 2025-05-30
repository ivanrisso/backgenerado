# ✅ app/services/tipocomprobante_service.py

from typing import List
from app.use_cases.tipocomprobante_use_case import TipoComprobanteUseCase
from app.schemas.tipocomprobante import TipoComprobanteCreate, TipoComprobanteUpdate, TipoComprobanteResponse
from app.domain.entities.tipocomprobante import TipoComprobante
from app.domain.exceptions.tipocomprobante import TipoComprobanteNoEncontrado, TipoComprobanteDuplicado
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class TipoComprobanteService:
    def __init__(self, use_case: TipoComprobanteUseCase):
        self.use_case = use_case

    def to_response(self, tipocomprobante: TipoComprobante) -> TipoComprobanteResponse:
        return TipoComprobanteResponse(**tipocomprobante.__dict__)

    async def get_by_id(self, id: int) -> TipoComprobanteResponse:
        try:
            tipocomprobante = await self.use_case.get_by_id(id)
            return self.to_response(tipocomprobante)
        except TipoComprobanteNoEncontrado as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al obtener tipocomprobante")

    async def get_all(self) -> List[TipoComprobanteResponse]:
        try:
            tipocomprobantes = await self.use_case.get_all()
            return [self.to_response(c) for c in tipocomprobantes]
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al listar tipocomprobantes")

    async def create(self, data: TipoComprobanteCreate) -> TipoComprobanteResponse:
        try:
            tipocomprobante = await self.use_case.create(data)
            return self.to_response(tipocomprobante)
        except (TipoComprobanteDuplicado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear tipocomprobante")

    async def update(self, id: int, data: TipoComprobanteUpdate) -> TipoComprobanteResponse:
        try:
            tipocomprobante = await self.use_case.update(id, data)
            return self.to_response(tipocomprobante)
        except (TipoComprobanteNoEncontrado, TipoComprobanteDuplicado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al actualizar tipocomprobante")

    async def delete(self, id: int) -> None:
        try:
            await self.use_case.delete(id)
        except (TipoComprobanteNoEncontrado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar tipocomprobante")
