# ✅ app/use_cases/comprobante_full_use_case.py

import logging
from app.schemas.comprobante_full import ComprobanteFullCreate
from app.domain.entities.comprobante_full import ComprobanteFull
from app.domain.entities.comprobante import Comprobante
from app.domain.entities.comprobantedetalle import ComprobanteDetalle
from app.domain.entities.comprobanteimpuesto import ComprobanteImpuesto
from app.adapters.afip_adapter import AfipAdapter
from app.domain.exceptions.base import ErrorDeRepositorio
from app.repositories.comprobante_full_repository import ComprobanteFullUOW

logger = logging.getLogger(__name__)


class ComprobanteFullUseCase:
    def __init__(
        self,
        uow: ComprobanteFullUOW,
        afip_adapter: AfipAdapter
    ):
        self.uow = uow
        self.afip_adapter = afip_adapter

    async def create_comprobante_full(self, payload: ComprobanteFullCreate) -> ComprobanteFull:
        try:
            async with self.uow:
                # Crear cabecera
                cabecera = Comprobante.from_create_schema(payload)
                cabecera = await self.uow.comprobante_repo.create(cabecera, commit=False)

                # Crear detalles
                detalles = []
                for d in payload.detalles:
                    detalle = ComprobanteDetalle.from_create(d, cabecera.id)
                    await self.uow.comprobante_detalle_repo.create(detalle, commit=False)
                    detalles.append(detalle)

                # Crear impuestos
                impuestos = []
                for i in payload.impuestos:
                    impuesto = ComprobanteImpuesto.from_create(i, cabecera.id)
                    await self.uow.comprobante_impuesto_repo.create(impuesto, commit=False)
                    impuestos.append(impuesto)

                # Solicitar CAE
                cae_info = await self.afip_adapter.solicitar_cae(payload, cabecera)
                cabecera.cae = cae_info["CAE"]
                cabecera.cae_vencimiento = cae_info["CAEFchVto"]
                await self.uow.comprobante_repo.update(cabecera.id, cabecera, commit=False)

                await self.uow.commit()

                return ComprobanteFull(cabecera, detalles, impuestos)

        except Exception as e:
            logger.exception("Error inesperado al crear comprobante completo")
            raise ErrorDeRepositorio("Error inesperado al crear comprobante completo")
