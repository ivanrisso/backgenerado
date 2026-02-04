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
from typing import Any

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
        condicion_iva_uc: Any, # CondicionIvaUseCase (Dynamic typing to avoid circular imports if needed)
        iva_rates_uc: IvaUseCase
    ):
        self.ebilling = ebilling
        self.tipo_comprobante_uc = tipo_comprobante_uc
        self.concepto_uc = concepto_uc
        self.tipodoc_uc = tipodoc_uc
        self.moneda_uc = moneda_uc
        self.cliente_uc = cliente_uc
        self.iva_uc = condicion_iva_uc # Use proper naming internally if possible, keeping backwards compat var name might be confusing.
        self.condicion_iva_uc = condicion_iva_uc
        self.iva_rates_uc = iva_rates_uc

    async def solicitar_cae(self, payload: ComprobanteFullCreate, comprobante: Comprobante) -> dict:
        # Validar número de documento
        try:
            with open("/tmp/afip_debug.log", "a") as f:
                 f.write(f"DEBUG ENTER solicitar_cae. ClienteID: {comprobante.cliente_id}\n")
        except:
            pass

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
            
            # Use condicion_iva_uc (GetCondicionIvaByIdUseCase) injected as iva_uc for now, 
            # OR better: use the one finding logic directly if passed correctly.
            # Ideally we rename the dependency, but for minimal changes let's assume iva_uc is now the correct one
            # OR we simply fix the usage here if we change the injection.
            
            if not cliente.condicion_iva_id:
                raise ErrorAfip(f"El cliente {cliente.nombre} no tiene condición de IVA asignada")

            # Fetch Condicion Entity
            # NOTE: We can pass Repository directly which has get_by_id
            condicion_iva = await self.condicion_iva_uc.get_by_id(cliente.condicion_iva_id) 
            
            if not condicion_iva:
                 raise ErrorAfip(f"No se encontró la condición de IVA ID {cliente.condicion_iva_id}")

        except Exception as e:
            try:
                with open("/tmp/afip_debug.log", "a") as f:
                     f.write(f"DEBUG EXCEPTION METADATA: {str(e)}\n")
            except:
                pass
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
        
        # Logging debug info to file for visibility
        try:
            with open("/tmp/afip_debug.log", "a") as f:
                 f.write(f"DEBUG STARTING CAE. Concepto: {concepto.codigo_arca}\n")
        except:
            pass

        # Fix types for Zeep (WSDL expects ints for IDs)
        try:
            c_concepto = int(concepto.codigo_arca)
            c_doctipo = int(tipo_doc.codigo_arca)
            c_moneda = str(moneda.codigo_arca) # Currency code is string 'PES'
        except ValueError:
             raise ErrorAfip(f"Error convirtiendo códigos ARCA a int. Concepto={concepto.codigo_arca}, DocTipo={tipo_doc.codigo_arca}")

        # Detalle
        detalle_req = {
            "Concepto": c_concepto,
            "DocTipo": c_doctipo,
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
            "MonId": c_moneda,
            "MonCotiz": payload.cotizacion_moneda
        }

        # RG 5616: Condicion IVA Receptor - Mapeo Manual si falta codigo
        codigo_condicion = None
        
        # Intentar obtener del modelo si tuviera campo codigo (no tiene aun)
        if hasattr(condicion_iva, 'codigo') and condicion_iva.codigo is not None:
             codigo_condicion = condicion_iva.codigo
        else:
             # Map by Name (Fallback)
             nombre_cond = condicion_iva.nombre.lower() if condicion_iva.nombre else ""
             if "inscripto" in nombre_cond:
                 codigo_condicion = 1
             elif "monotributo" in nombre_cond:
                 codigo_condicion = 6
             elif "exento" in nombre_cond:
                 codigo_condicion = 4
             elif "consumidor final" in nombre_cond:
                 codigo_condicion = 5
        
        if codigo_condicion is None:
             # Default fallback or Error? AFIP requires it.
             # Let's default to Consumidor Final (5) if unknown to avoid blocking, OR error.
             # Error is safer.
             raise ErrorAfip(f"No se pudo determinar código AFIP para condición '{condicion_iva.nombre}'")
             
        detalle_req["CondicionIVAReceptorId"] = codigo_condicion

        # Fechas del servicio (solo si concepto no es Productos)
        # Concepto 1 = Productos (no requiere fechas)
        # Concepto 2 = Servicios (requiere fechas)
        # Concepto 3 = Prod y Serv
        # Fix check logic (integers)
        if c_concepto in [2, 3]:
            detalle_req["FchServDesde"] = payload.fecha_emision.strftime("%Y%m%d") # Should be actual dates
            detalle_req["FchServHasta"] = payload.fecha_emision.strftime("%Y%m%d")
            detalle_req["FchVtoPago"] = payload.fecha_emision.strftime("%Y%m%d")


        if payload.detalles:
            try:
                # Group by AFIP Code
                iva_aggregates = {} # { afip_code: { BaseImp: X, Importe: Y, Id: afip_code } }
                
                # Use list comprehension to get unique IDs, ensuring we filter None
                unique_iva_ids = set(d.iva_id for d in payload.detalles if d.iva_id is not None)
                iva_map = {} # id -> codigo
                
                with open("/tmp/afip_debug.log", "a") as f:
                    f.write(f"DEBUG Unique IVA IDs: {unique_iva_ids}\n")

                for iid in unique_iva_ids:
                     # Ensure this calls the RATES use case
                     if not self.iva_rates_uc:
                         raise Exception("iva_rates_uc dependency is missing in Adapter")
                         
                     iva_ent = await self.iva_rates_uc.get_by_id(iid)
                     if iva_ent and iva_ent.codigo is not None:
                        iva_map[iid] = int(iva_ent.codigo) # Zeep prefers int for ID
                     else:
                        raise ErrorAfip(f"IVA ID {iid} no tiene código AFIP asociado")
    
                # 2. Iterate details and aggregate
                for d in payload.detalles:
                    if d.iva_id is not None:
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
                
            except Exception as iv_ex:
                 with open("/tmp/afip_debug.log", "a") as f:
                    f.write(f"DEBUG IVA PROCESS EXCEPTION: {iv_ex}\n")
                 raise ErrorAfip(f"Error procesando IVAs: {str(iv_ex)}")

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
                "CbteTipo": c_concepto # Wait, CbteTipo is Tipo Comprobante (e.g. 1, 6), NOT Concepto!
            },
            "FeDetReq": [detalle_req] 
        }
        
        # FIX: CbteTipo should be Tipo Comprobante code, not Concepto code.
        # Original code line 183: "CbteTipo": tipo_cbte.codigo_arca
        payload_req["FeCabReq"]["CbteTipo"] = int(tipo_cbte.codigo_arca)

        logger.info(f"DEBUG AFIP PAYLOAD: PtoVta={comprobante.punto_venta}, Tipo={tipo_cbte.codigo_arca}, Detalle={detalle_req}")
        
        # Solicitar CAE
        try:
            with open("/tmp/afip_debug.log", "a") as f:
                 f.write(f"DEBUG Sending Payload: {payload_req}\n")

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
            with open("/tmp/afip_debug.log", "a") as f:
                 f.write(f"DEBUG AFIP EXCEPTION: {e}\n")
            raise ErrorAfip(
                mensaje="Error al solicitar CAE a AFIP",
                causa=str(e)
            )
