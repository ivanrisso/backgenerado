# app/adapters/afip_adapter.py

from fastapi import HTTPException
from app.schemas.comprobante_full import ComprobanteFullCreate
from app.domain.entities.comprobante import Comprobante
from app.use_cases.tipocomprobante_use_case import TipoComprobanteUseCase 
from app.use_cases.concepto_use_case import ConceptoUseCase
from app.use_cases.tipodoc_use_case import TipoDocUseCase
from app.use_cases.moneda_use_case import MonedaUseCase

class AfipAdapter:
    def __init__(self, afip_sdk):
        self.afip = afip_sdk

    async def solicitar_cae(self, payload: ComprobanteFullCreate, comprobante: Comprobante):
        try:
            doc_nro = int(payload.doc_nro)
        except ValueError:
            raise HTTPException(status_code=422, detail="doc_nro inválido")
        
        tipo_cbte = await TipoComprobanteUseCase.get_by_id(comprobante.tipo_comprobante_id)
        concepto = await ConceptoUseCase.get_by_id(comprobante.concepto_id)
        tipo_doc = await TipoDocUseCase.get_by_id(comprobante.tipo_doc_id)
        moneda = await MonedaUseCase.get_by_id(comprobante.moneda_id)

        data = {
            "CantReg": 1,
            "PtoVta": comprobante.punto_venta,
            "CbteTipo": tipo_cbte.codigo_arca,
            "Concepto": concepto.codigo_arca,
            "DocTipo": tipo_doc.codigo_arca,
            "DocNro": doc_nro,
            "CbteDesde": comprobante.numero,
            "CbteHasta": comprobante.numero,
            "CbteFch": payload.fecha_emision.strftime("%Y%m%d"),
            "ImpTotal": payload.total,
            "ImpTotConc": 0,
            "ImpNeto": payload.total_neto,
            "ImpOpEx": 0,
            "ImpIVA": payload.total_iva,
            "ImpTrib": payload.total_impuestos,
            "MonId": moneda.codigo_arca,
            "MonCotiz": payload.cotizacion_moneda,
        }

        if payload.detalles:
            data["Iva"] = [
                {"Id": d.iva_id, "BaseImp": d.importe, "Importe": d.importe_iva}
                for d in payload.detalles if d.iva_id
            ]

        if payload.impuestos:
            data["Tributos"] = [
                {"Id": i.tipo_impuesto_id, "BaseImp": i.base_imponible, "Importe": i.importe}
                for i in payload.impuestos
            ]

        try:
            return self.afip.ElectronicBilling.createVoucher(data)
        except Exception as e:
            raise HTTPException(502, f"Error al solicitar CAE: {str(e)}")
