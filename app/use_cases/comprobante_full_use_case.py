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

                # Asignar CAE antes de persistir
                cabecera.cae = cae_info["CAE"]
                from datetime import datetime
                # AFIP returns YYYYMMDD string
                vto = cae_info["CAEFchVto"]
                if isinstance(vto, str):
                    cabecera.cae_vencimiento = datetime.strptime(vto, "%Y%m%d").date()
                else:
                    cabecera.cae_vencimiento = vto

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
                # Note: We already set this before create, so this update is technically redundant unless we want to be safe.
                # But since we use same obj... 
                
                # ------ Lógica de Imputación Automática (Cuenta Corriente) ------
                if hasattr(payload, "cbtes_asociados") and payload.cbtes_asociados:
                    from app.domain.entities.imputacion import Imputacion
                    
                    for assoc in payload.cbtes_asociados:
                        # 1. Buscar Comprobante Local
                        try:
                            invoice = await self.uow.comprobante_repo.get_by_afip_data(
                                codigo_arca=str(assoc.Tipo).zfill(3), # Ensure 3 digits (e.g. 11 -> 011)
                                punto_venta=assoc.PtoVta,
                                numero=assoc.Nro
                            )
                            
                            if invoice:
                                # 2. Calcular importe a imputar
                                # Por defecto, tomamos el total de la NC (o lo que quede de saldo)
                                # Si el usuario especifica importe_imputar > 0, intentamos usar eso.
                                
                                monto_imputar = 0.0
                                
                                # Lógica de Imputación Parcial (HF-GAP-001)
                                if getattr(assoc, 'importe_imputar', 0) > 0:
                                    solicitado = assoc.importe_imputar
                                    
                                    # Validaciones
                                    if solicitado > invoice.saldo:
                                        raise HTTPException(status_code=400, detail=f"El importe a imputar ({solicitado}) excede el saldo de la factura ({invoice.saldo})")
                                    
                                    if solicitado > cabecera.saldo:
                                        raise HTTPException(status_code=400, detail=f"El importe a imputar ({solicitado}) excede el saldo disponible de la NC ({cabecera.saldo})")
                                        
                                    monto_imputar = solicitado
                                else:
                                    # Lógica por defecto (Automática)
                                    monto_imputar = min(invoice.saldo, cabecera.saldo)
                                
                                if monto_imputar > 0:
                                    # 3. Crear Imputacion
                                    imputacion = Imputacion(
                                        id=None,
                                        comprobante_credito_id=cabecera.id, # La NC que acabamos de crear
                                        comprobante_debito_id=invoice.id,
                                        importe=monto_imputar,
                                        fecha=cabecera.fecha_emision
                                    )
                                    await self.uow.imputacion_repo.create(imputacion, commit=False)
                                    
                                    # 4. Actualizar Saldos
                                    invoice.saldo -= monto_imputar
                                    cabecera.saldo -= monto_imputar
                                    
                                    # Persistir cambios en saldos
                                    await self.uow.comprobante_repo.update(invoice.id, invoice, commit=False)
                                    await self.uow.comprobante_repo.update(cabecera.id, cabecera, commit=False)
                                    
                                    logger.info(f"Imputación creada: NC {cabecera.id} -> Factura {invoice.id} por {monto_imputar}")
                                    
                        except HTTPException:
                            raise
                        except Exception as integrity_ex:
                             logger.error(f"Error al imputar comprobante asociado: {integrity_ex}")
                             # No bloqueamos la creación de la NC, solo logueamos (para errores no críticos).

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

        except Exception as e:
            logger.exception("Error inesperado al crear comprobante completo")
            raise ErrorDeRepositorio(f"Error inesperado al crear comprobante completo: {str(e)}")
