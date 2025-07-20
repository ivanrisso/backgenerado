# app/adapters/afip_adapter.py

from app.schemas.comprobante_full import ComprobanteFullCreate
from app.domain.entities.comprobante import Comprobante
from app.use_cases.tipocomprobante_use_case import TipoComprobanteUseCase
from app.use_cases.concepto_use_case import ConceptoUseCase
from app.use_cases.tipodoc_use_case import TipoDocUseCase
from app.use_cases.moneda_use_case import MonedaUseCase
from app.domain.exceptions.afip import ErrorAfip
from afip.electronic_billing import ElectronicBilling
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class AfipAdapter:
    def __init__(
        self,
        ebilling: ElectronicBilling,
        tipo_comprobante_uc: TipoComprobanteUseCase,
        concepto_uc: ConceptoUseCase,
        tipodoc_uc: TipoDocUseCase,
        moneda_uc: MonedaUseCase
    ):
        self.ebilling = ebilling
        self.tipo_comprobante_uc = tipo_comprobante_uc
        self.concepto_uc = concepto_uc
        self.tipodoc_uc = tipodoc_uc
        self.moneda_uc = moneda_uc

    async def solicitar_cae(self, payload: ComprobanteFullCreate, comprobante: Comprobante) -> dict:
        # Validar número de documento
        try:
            doc_nro = int(payload.doc_nro)
        except ValueError:
            raise ErrorAfip("El número de documento (doc_nro) no es válido")

        # Resolver metadata
        try:
            tipo_cbte = await self.tipo_comprobante_uc.get_by_id(comprobante.tipo_comprobante_id)
            concepto = await self.concepto_uc.get_by_id(comprobante.concepto_id)
            tipo_doc = await self.tipodoc_uc.get_by_id(comprobante.tipo_doc_id)
            moneda = await self.moneda_uc.get_by_id(comprobante.moneda_id)
        except Exception as e:
            raise ErrorAfip("Error al obtener metadata para comprobante", causa=str(e))

        print(tipo_cbte)    

        if tipo_cbte.codigo_arca is None:
            raise ErrorAfip(
                mensaje="El tipo de comprobante no tiene código ARCA",
                causa=f"tipo_comprobante_id={comprobante.tipo_comprobante_id} no tiene código_arca definido"
            )

        # Obtener último número de comprobante
        try:
            print("➡️ Obteniendo último comprobante...")
            print(f"PtoVta: {comprobante.punto_venta} ({type(comprobante.punto_venta)})")
            print(f"CbteTipo: {tipo_cbte.codigo_arca} ({type(tipo_cbte.codigo_arca)})")            
            
            last_voucher = self.ebilling.getLastVoucher(comprobante.punto_venta, tipo_cbte.codigo_arca)
            comprobante.numero = last_voucher + 1
        except Exception as e:
            print(str(e))
            raise ErrorAfip(
                mensaje="Error al obtener último número de comprobante",
                causa=str(e)
            )
            
        # Construcción de payload
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
            "FchServDesde": payload.fecha_emision.strftime("%Y%m%d"),
            "FchServHasta": payload.fecha_emision.strftime("%Y%m%d"),
            "FchVtoPago": payload.fecha_emision.strftime("%Y%m%d"),
            "ImpTotal": payload.total,
            "ImpTotConc": 0,
            "ImpNeto": payload.total_neto,
            "ImpOpEx": 0,
            "ImpIVA": payload.total_iva,
            "ImpTrib": payload.total_impuestos,
            "MonId": moneda.codigo_arca,
            "MonCotiz": payload.cotizacion_moneda,
            "CondicionIVAReceptorId" : 1 
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

        # Solicitar CAE
        try:
            response = self.ebilling.createVoucher(data)
            return response
        except Exception as e:
            logger.exception("Error al solicitar CAE con payload: %s", data)
            raise ErrorAfip(
                mensaje="Error al solicitar CAE a AFIP",
                causa=str(e)
            )
