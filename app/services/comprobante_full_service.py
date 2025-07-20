# ✅ app/services/comprobante_full_service.py

import logging
from fastapi import HTTPException

from app.schemas.comprobante_full import ComprobanteFullCreate, ComprobanteFullResponse
from app.domain.entities.comprobante_full import ComprobanteFull
from app.use_cases.comprobante_full_use_case import ComprobanteFullUseCase

# Excepciones
from app.domain.exceptions.afip import ErrorAfip
from app.domain.exceptions.base import ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
from app.domain.exceptions.tipocomprobante import TipoComprobanteNoEncontrado
from app.domain.exceptions.concepto import ConceptoNoEncontrado
from app.domain.exceptions.moneda import MonedaNoEncontrado
from app.domain.exceptions.tipodoc import TipoDocNoEncontrado

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

        except (
            ErrorAfip,
            HTTPException,
            ClaveForaneaInvalida,
            TipoComprobanteNoEncontrado,
            ConceptoNoEncontrado,
            MonedaNoEncontrado,
            TipoDocNoEncontrado
        ) as e:
            raise e  # Propagar directamente a FastAPI

        except Exception:
            logger.exception("Error inesperado en servicio de comprobante full")
            raise ErrorDeRepositorio("Error inesperado al crear comprobante completo")

