# ✅ app/services/auditoriacomprobante_service.py

from typing import List
from app.use_cases.auditoriacomprobante_use_case import AuditoriaComprobanteUseCase
from app.schemas.auditoria_comprobante import AuditoriaComprobanteCreate, AuditoriaComprobanteUpdate, AuditoriaComprobanteResponse
from app.domain.entities.auditoriacomprobante import AuditoriaComprobante
from app.domain.exceptions.auditoriacomprobante import AuditoriaComprobanteNoEncontrado, AuditoriaComprobanteDuplicado, AuditoriaComprobanteInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class AuditoriaComprobanteService:
    def __init__(self, use_case: AuditoriaComprobanteUseCase):
        self.use_case = use_case

    def to_response(self, auditoriacomprobante: AuditoriaComprobante) -> AuditoriaComprobanteResponse:
        return AuditoriaComprobanteResponse(**auditoriacomprobante.__dict__)

    async def get_by_id(self, id: int) -> AuditoriaComprobanteResponse:
        try:
            auditoriacomprobante = await self.use_case.get_by_id(id)
            return self.to_response(auditoriacomprobante)
        except AuditoriaComprobanteNoEncontrado as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al obtener auditoriacomprobante")

    async def get_all(self) -> List[AuditoriaComprobanteResponse]:
        try:
            auditoriacomprobantes = await self.use_case.get_all()
            return [self.to_response(c) for c in auditoriacomprobantes]
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al listar auditoriacomprobantes")

    async def create(self, data: AuditoriaComprobanteCreate) -> AuditoriaComprobanteResponse:
        try:
            auditoriacomprobante = await self.use_case.create(data)
            return self.to_response(auditoriacomprobante)
        except (AuditoriaComprobanteDuplicado, ClaveForaneaInvalida, AuditoriaComprobanteInvalido) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear auditoriacomprobante")

    async def update(self, id: int, data: AuditoriaComprobanteUpdate) -> AuditoriaComprobanteResponse:
        try:
            auditoriacomprobante = await self.use_case.update(id, data)
            return self.to_response(auditoriacomprobante)
        except (AuditoriaComprobanteNoEncontrado, AuditoriaComprobanteDuplicado, ClaveForaneaInvalida, AuditoriaComprobanteInvalido) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al actualizar auditoriacomprobante")

    async def delete(self, id: int) -> None:
        try:
            await self.use_case.delete(id)
        except (AuditoriaComprobanteNoEncontrado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar auditoriacomprobante")
