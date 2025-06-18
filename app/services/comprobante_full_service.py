# ✅ app/services/comprobante_full_service.py

import logging
from app.schemas.comprobante_full import ComprobanteFullCreate, ComprobanteFullResponse
from app.domain.entities.comprobante_full import ComprobanteFull
from app.use_cases.comprobante_full_use_case import ComprobanteFullUseCase
from app.domain.exceptions.base import ErrorDeRepositorio
from app.domain.exceptions.afip import ErrorAfip
from app.domain.exceptions.integridad import ClaveForaneaInvalida

logger = logging.getLogger(__name__)


class ComprobanteFullService:
    def __init__(self, use_case: ComprobanteFullUseCase):
        self.use_case = use_case

    def to_response(self, full: ComprobanteFull) -> ComprobanteFullResponse:
        return ComprobanteFullResponse.from_domain(full)

    async def create_comprobante(self, payload: ComprobanteFullCreate) -> ComprobanteFullResponse:
        try:
            full = await self.use_case.create_comprobante_full(payload)
            return self.to_response(full)

        except (ErrorAfip, ClaveForaneaInvalida) as e:
            raise e

        except Exception as ex:
            logger.exception("Error inesperado al crear comprobante completo")
            raise ErrorDeRepositorio("Error inesperado al crear comprobante completo")
