# ✅ app/use_cases/comprobante_full_use_case.py

import logging
from fastapi import HTTPException

from app.schemas.comprobante_full import ComprobanteFullCreate
from app.domain.dtos.comprobante_dto import ComprobanteDTO
from app.domain.dtos.comprobante_detalle_dto import ComprobanteDetalleDTO
from app.domain.dtos.comprobante_impuesto_dto import ComprobanteImpuestoDTO
from app.domain.entities.comprobante_full import ComprobanteFull
from app.domain.entities.comprobante import Comprobante
from app.domain.entities.comprobantedetalle import ComprobanteDetalle
from app.domain.entities.comprobanteimpuesto import ComprobanteImpuesto
from app.adapters.afip_adapter import AfipAdapter
from app.repositories.comprobante_full_repository import ComprobanteFullUOW

# Excepciones
from app.domain.exceptions.afip import ErrorAfip
from app.domain.exceptions.base import ErrorDeRepositorio
from app.domain.exceptions.tipocomprobante import TipoComprobanteNoEncontrado
from app.domain.exceptions.concepto import ConceptoNoEncontrado
from app.domain.exceptions.moneda import MonedaNoEncontrado
from app.domain.exceptions.tipodoc import TipoDocNoEncontrado

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
                # Construcción del DTO
                dto = ComprobanteDTO(**payload.dict())
                cabecera = Comprobante.from_dto(dto)

                # Solicita CAE
                cae_info = await self.afip_adapter.solicitar_cae(payload, cabecera)

                # Persistencia de cabecera
                cabecera = await self.uow.comprobante_repo.create(cabecera, commit=False)
                await self.uow.flush()

                # Detalles
                detalles = []
                for d in payload.detalles:
                    data = d.model_dump()
                    data["comprobante_id"] = cabecera.id
                    detalle_dto = ComprobanteDetalleDTO(**data)
                    detalle = ComprobanteDetalle.from_dto(detalle_dto)
                    await self.uow.comprobante_detalle_repo.create(detalle, commit=False)
                    detalles.append(detalle)
                    
                # Impuestos
                impuestos = []
                for i in payload.impuestos:
                    data = i.model_dump()
                    data["comprobante_id"] = cabecera.id
                    impuesto_dto = ComprobanteImpuestoDTO(**data)
                    impuesto = ComprobanteImpuesto.from_dto(impuesto_dto)
                    await self.uow.comprobante_impuesto_repo.create(impuesto, commit=False)
                    impuestos.append(impuesto)

                # Actualización CAE
                cabecera.cae = cae_info["CAE"]
                cabecera.cae_vencimiento = cae_info["CAEFchVto"]
                await self.uow.comprobante_repo.update(cabecera.id, cabecera, commit=False)

                await self.uow.commit()
                
                logger.info("Comprobante creado: %s", cabecera.cae)

                
                return ComprobanteFull(cabecera, detalles, impuestos)

        except (
            ErrorAfip,
            HTTPException,
            TipoComprobanteNoEncontrado,
            ConceptoNoEncontrado,
            MonedaNoEncontrado,
            TipoDocNoEncontrado
        ) as ex:
            raise ex

        except Exception:
            logger.exception("Error inesperado al crear comprobante completo")
            raise ErrorDeRepositorio("Error inesperado al crear comprobante completo")
