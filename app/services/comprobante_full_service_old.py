# app/services/comprobante_full_service.py

import logging
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from afip import Afip

from app.schemas.comprobante_full import ComprobanteFullCreate
from app.domain.entities.comprobante import Comprobante
from app.domain.entities.comprobantedetalle import ComprobanteDetalle
from app.domain.entities.comprobanteimpuesto import ComprobanteImpuesto

from app.repositories.comprobante_repository import ComprobanteRepositoryImpl
from app.repositories.comprobantedetalle_repository import ComprobanteDetalleRepositoryImpl
from app.repositories.comprobanteimpuesto_repository import ComprobanteImpuestoRepositoryImpl

from app.use_cases.tipocomprobante_use_case import TipoComprobanteUseCase
from app.use_cases.concepto_use_case import ConceptoUseCase
from app.use_cases.tipodoc_use_case import TipoDocUseCase
from app.use_cases.moneda_use_case import MonedaUseCase


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class ComprobanteFullService:
    def __init__(self, db: AsyncSession, afip_client: Afip):
        self.db       = db
        self.afip     = afip_client
        self.repo     = ComprobanteRepositoryImpl(db)
        self.repo_det = ComprobanteDetalleRepositoryImpl(db)
        self.repo_imp = ComprobanteImpuestoRepositoryImpl(db)

    async def create(self, payload: ComprobanteFullCreate) -> Comprobante:
        async with self.db.begin():
            # 1) Cabecera
            domain_cab = Comprobante(
                id=None,
                cliente_id=payload.cliente_id,
                tipo_comprobante_id=payload.tipo_comprobante_id,
                concepto_id=payload.concepto_id,
                tipo_doc_id=payload.tipo_doc_id,
                moneda_id=payload.moneda_id,
                punto_venta=payload.punto_venta,
                numero=payload.numero,
                fecha_emision=payload.fecha_emision,
                doc_nro=payload.doc_nro,
                nombre_cliente=payload.nombre_cliente,
                domicilio_cliente=payload.domicilio_cliente,
                localidad_cliente=payload.localidad_cliente,
                cod_postal_cliente=payload.cod_postal_cliente,
                provincia_cliente=payload.provincia_cliente,
                cotizacion_moneda=payload.cotizacion_moneda,
                total_neto=payload.total_neto,
                total_iva=payload.total_iva,
                total_impuestos=payload.total_impuestos,
                total=payload.total,
                observaciones=payload.observaciones
            )
            created = await self.repo.create(domain_cab, commit=False)

            # 2) Detalles
            for det_dto in payload.detalles:
                domain_det = ComprobanteDetalle(
                    id=None,
                    comprobante_id=created.id,
                    descripcion=det_dto.descripcion,
                    cantidad=det_dto.cantidad,
                    precio_unitario=det_dto.precio_unitario,
                    importe=det_dto.importe
                )
                await self.repo_det.create(domain_det, commit=False)

            # 3) Impuestos
            for imp_dto in payload.impuestos:
                domain_imp = ComprobanteImpuesto(
                    id=None,
                    comprobante_id=created.id,
                    tipo_impuesto_id=imp_dto.tipo_impuesto_id,
                    descripcion=imp_dto.descripcion,
                    base_imponible=imp_dto.base_imponible,
                    alicuota=imp_dto.alicuota,
                    importe=imp_dto.importe
                )
                await self.repo_imp.create(domain_imp, commit=False)

            try:
                doc_nro_int = int(payload.doc_nro)
            except ValueError:
                raise HTTPException(
                    status_code=422,
                    detail="doc_nro inválido: debe ser cadena de dígitos"
                )
            
            # 2) Cargar entidades de referencia para códigos AFIP
            tipo_cbte = await TipoComprobanteUseCase.get_by_id(created.tipo_comprobante_id)
            concepto  = await ConceptoUseCase.get_by_id(created.concepto_id)
            tipo_doc  = await TipoDocUseCase.get_by_id(created.tipo_doc_id)
            moneda    = await MonedaUseCase.get_by_id(created.moneda_id)
                         
            
            # 4) Armo el payload para AFIP
            data_afip = {
                "CantReg":  1,
                "PtoVta":   created.punto_venta,
                "CbteTipo": tipo_cbte.codigo_arca,
                "Concepto":   concepto.codigo_arca,
                "DocTipo":    tipo_doc.codigo_arca,
                "DocNro":     doc_nro_int, #payload.doc_nro, 
                "CbteDesde":  created.numero,
                "CbteHasta":  created.numero,
                "CbteFch":    payload.fecha_emision.strftime("%Y%m%d"),
                "ImpTotal":   payload.total,
                "ImpTotConc": 0,
                "ImpNeto":    payload.total_neto,
                "ImpOpEx":    0,
                "ImpIVA":     payload.total_iva,
                "ImpTrib":    payload.total_impuestos,
                "MonId":      moneda.codigo_arca,
                "MonCotiz":   payload.cotizacion_moneda,                                
            }
            
            # Si tienes varios detalles de IVA:
            if payload.detalles:
                data_afip["Iva"] = [
                    {
                        "Id": det.iva_id,
                        "BaseImp": det.importe,
                        "Importe": det.importe_iva,
                    }
                    for det in payload.detalles
                    if det.iva_id is not None
                ]
                
            # Si tienes tributos adicionales:
            if payload.impuestos:
                data_afip["Tributos"] = [
                    {
                        "Id": imp.tipo_impuesto_id,
                        "BaseImp": imp.base_imponible,
                        "Importe": imp.importe,
                    }
                    for imp in payload.impuestos
                ]
                                                
            # 5) Llamás al SDK
            try:
                cae_response = self.afip.ElectronicBilling.createVoucher(data_afip)
                created.cae = cae_response["CAE"]
                created.cae_vencimiento = cae_response["CAEFchVto"]
            except Exception as e:
                logger.error("Error al solicitar CAE a AFIP: %s", e)
                raise HTTPException(
                    status.HTTP_502_BAD_GATEWAY,
                    detail="Error en AFIP WSFE: " + str(e)
                )

            # 8) Guardar CAE en BD
            await self.repo.update(created.id, created, commit=False)

        return created
