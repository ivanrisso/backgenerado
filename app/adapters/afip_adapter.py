# app/adapters/afip_adapter.py

import logging
from app.schemas.comprobante_full import ComprobanteFullCreate
from app.domain.entities.comprobante import Comprobante
from app.use_cases.tipocomprobante_use_case import TipoComprobanteUseCase
from app.use_cases.concepto_use_case import ConceptoUseCase
from app.use_cases.tipodoc_use_case import TipoDocUseCase
from app.use_cases.moneda_use_case import MonedaUseCase
from app.use_cases.cliente_use_case import ClienteUseCase
from app.use_cases.iva_use_case import IvaUseCase
from app.domain.exceptions.afip import ErrorAfip
from app.core.afip.wsfe import WSFEClient

logger = logging.getLogger(__name__)

class AfipAdapter:
    def __init__(
        self,
        ebilling: WSFEClient,
        tipo_comprobante_uc: TipoComprobanteUseCase,
        concepto_uc: ConceptoUseCase,
        tipodoc_uc: TipoDocUseCase,

        moneda_uc: MonedaUseCase,
        cliente_uc: ClienteUseCase,
        iva_uc: IvaUseCase
    ):
        self.ebilling = ebilling
        self.tipo_comprobante_uc = tipo_comprobante_uc
        self.concepto_uc = concepto_uc
        self.tipodoc_uc = tipodoc_uc
        self.moneda_uc = moneda_uc
        self.cliente_uc = cliente_uc
        self.iva_uc = iva_uc

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
            
            # Nuevo: RG 5616 - Obtener datos del cliente e IVA
            cliente = await self.cliente_uc.get_by_id(comprobante.cliente_id)
            if not cliente:
                 raise ErrorAfip(f"Cliente {comprobante.cliente_id} no encontrado")
            
            condicion_iva = await self.iva_uc.get_by_id(cliente.condicion_iva_id)
            if not condicion_iva:
                 raise ErrorAfip(f"El cliente {cliente.nombre} no tiene condición de IVA asignada")

        except Exception as e:
            raise ErrorAfip("Error al obtener metadata para comprobante", causa=str(e))

        if tipo_cbte.codigo_arca is None:
            raise ErrorAfip(
                mensaje="El tipo de comprobante no tiene código ARCA",
                causa=f"tipo_comprobante_id={comprobante.tipo_comprobante_id} no tiene código_arca definido"
            )

        # Obtener último número de comprobante
        try:
            logger.info(f"➡️ Obteniendo último comprobante... PtoVta: {comprobante.punto_venta}, Tipo: {tipo_cbte.codigo_arca}")
            
            last_voucher = self.ebilling.get_last_voucher(comprobante.punto_venta, tipo_cbte.codigo_arca)
            comprobante.numero = last_voucher + 1
        except Exception as e:
            raise ErrorAfip(
                mensaje="Error al obtener último número de comprobante",
                causa=str(e)
            )
            
        # Construcción de payload (Estructura hierarchy Zeep)
        
        # Detalle
        detalle_req = {
            "Concepto": concepto.codigo_arca,
            "DocTipo": tipo_doc.codigo_arca,
            "DocNro": doc_nro,
            "CbteDesde": comprobante.numero,
            "CbteHasta": comprobante.numero,
            "CbteFch": payload.fecha_emision.strftime("%Y%m%d"),
            "ImpTotal": payload.total,
            "ImpTotConc": 0, # No gravado
            "ImpNeto": payload.total_neto,
            "ImpOpEx": 0,    # Exento
            "ImpIVA": payload.total_iva,
            "ImpTrib": payload.total_impuestos,
            "MonId": moneda.codigo_arca,
            "MonCotiz": payload.cotizacion_moneda
        }

        # RG 5616: Condicion IVA Receptor
        if condicion_iva.codigo is None:
             raise ErrorAfip(f"La condición de IVA '{condicion_iva.descripcion}' no tiene código ARCA asociado")
             
        detalle_req["CondicionIVAReceptorId"] = condicion_iva.codigo

        # Fechas del servicio (solo si concepto no es Productos)
        # Concepto 1 = Productos (no requiere fechas)
        # Concepto 2 = Servicios (requiere fechas)
        # Concepto 3 = Prod y Serv
        if concepto.codigo_arca in [2, 3]:
            detalle_req["FchServDesde"] = payload.fecha_emision.strftime("%Y%m%d") # Should be actual dates
            detalle_req["FchServHasta"] = payload.fecha_emision.strftime("%Y%m%d")
            detalle_req["FchVtoPago"] = payload.fecha_emision.strftime("%Y%m%d")


        if payload.detalles:
            # Group by AFIP Code
            iva_aggregates = {} # { afip_code: { BaseImp: X, Importe: Y, Id: afip_code } }
            
            for d in payload.detalles:
                if d.iva_id:
                     # Fetch Iva entity. 
                     # Option A: Fetch one by one (slow but easy)
                     # Option B: Fetch all relevant (better)
                     # Since this is async loop, one by one is O(N).
                     # Optimization: Cache fetched IVAs in local dict
                     
                     # Check if we already fetched this iva_id?
                     # Since I cannot easily maintain state across loop without pre-fetching.
                     pass 
            
            # Better approach: 
            # 1. Collect all unique IVA IDs
            unique_iva_ids = set(d.iva_id for d in payload.detalles if d.iva_id)
            iva_map = {} # id -> codigo
            
            for iid in unique_iva_ids:
                iva_ent = await self.iva_uc.get_by_id(iid)
                if iva_ent and iva_ent.codigo is not None:
                    iva_map[iid] = iva_ent.codigo
                else:
                    raise ErrorAfip(f"IVA ID {iid} no tiene código AFIP asociado")

            # 2. Iterate details and aggregate
            for d in payload.detalles:
                if d.iva_id:
                    afip_code = iva_map.get(d.iva_id)
                    if afip_code not in iva_aggregates:
                        iva_aggregates[afip_code] = {"Id": afip_code, "BaseImp": 0.0, "Importe": 0.0}
                    
                    iva_aggregates[afip_code]["BaseImp"] += d.importe
                    iva_aggregates[afip_code]["Importe"] += d.importe_iva
            
            # 3. Convert to List
            detalle_req["Iva"] = {
                 "AlicIva": list(iva_aggregates.values())
            }
            logger.info(f"DEBUG ALICIVA: {detalle_req['Iva']}")
            print(f"DEBUG ALICIVA PAYLOAD: {detalle_req['Iva']}")

        if payload.impuestos:
             detalle_req["Tributos"] = {
                 "Tributo": [
                    {"Id": i.tipo_impuesto_id, "BaseImp": i.base_imponible, "Importe": i.importe}
                    for i in payload.impuestos
                 ]
             }


        if hasattr(payload, "cbtes_asociados") and payload.cbtes_asociados:
             detalle_req["CbtesAsoc"] = {
                 "CbteAsoc": [
                     {"Tipo": c.Tipo, "PtoVta": c.PtoVta, "Nro": c.Nro}
                     for c in payload.cbtes_asociados
                 ]
             }

        payload_req = {
            "FeCabReq": {
                "CantReg": 1,
                "PtoVta": comprobante.punto_venta,
                "CbteTipo": tipo_cbte.codigo_arca
            },
            "FeDetReq": [detalle_req] 
        }
        
        logger.info(f"DEBUG AFIP PAYLOAD: PtoVta={comprobante.punto_venta}, Tipo={tipo_cbte.codigo_arca}, Detalle={detalle_req}")
        print(f"DEBUG AFIP PAYLOAD: PtoVta={comprobante.punto_venta}, Tipo={tipo_cbte.codigo_arca}, Detalle={detalle_req}")

        # Solicitar CAE
        try:
            response = self.ebilling.create_voucher(payload_req)
            
            det_resp = response.FeDetResp.FECAEDetResponse[0]
            if det_resp.Resultado == "R": # Rechazado
                 # Collect observations
                 obs = ""
                 if det_resp.Observaciones:
                     obs = "; ".join([f"{o.Code}: {o.Msg}" for o in det_resp.Observaciones.Obs])
                 raise Exception(f"AFIP rechazó el comprobante: {obs}")

            return {
                "CAE": det_resp.CAE,
                "CAEFchVto": det_resp.CAEFchVto 
            }
            
        except Exception as e:
            logger.exception("Error al solicitar CAE")
            raise ErrorAfip(
                mensaje="Error al solicitar CAE a AFIP",
                causa=str(e)
            )
