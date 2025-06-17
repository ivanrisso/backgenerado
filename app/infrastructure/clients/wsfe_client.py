# src/infrastructure/clients/wsfe_client.py
import os
from zeep import Client, Settings
from zeep.plugins import HistoryPlugin
from typing import Dict, Any

class WsfeClient:
    def __init__(self, token: str, sign: str):
        wsdl = os.getenv("WSFE_WSDL")
        settings = Settings(strict=False, xml_huge_tree=True)
        self.history = HistoryPlugin()
        self.client = Client(wsdl, settings=settings, plugins=[self.history])
        self.auth = {
            "Token": token,
            "Sign":  sign,
            "Cuit":  int(os.getenv("CUIT"))
        }

    def emitir_factura(self, cae_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ejecuta FECAESolicitar contra AFIP.
        cae_request debe incluir:
         - FeCabReq: CantReg, PtoVta, CbteTipo
         - FeDetReq: FECAEDetRequest con datos de la factura
        """
        response = self.client.service.FECAESolicitar(
            feAuth=self.auth,
            arrayFeCAERequest={"FeCAERequest": cae_request}
        )
        # Navegar la respuesta para extraer CAE y datos
        res = response.Resultado.FECAEResponse
        return {
            "CAE":       res.CAE,
            "vtoCae":    res.CAEFchVto,
            "observaciones": [
                { "code": o.Code, "msg": o.Msg }
                for o in getattr(res, "Observaciones", []) or []
            ]
        }

    def consultar_estado(self, punto_venta: int, tipo_cbte: int, nro_cbte: int) -> Dict[str, Any]:
        """
        Ejecuta FECompConsultar para verificar estado de un comprobante ya emitido.
        """
        request = {
            "FeCompConsReq": {
                "CbteNro":     nro_cbte,
                "PtoVta":      punto_venta,
                "CbteTipo":    tipo_cbte
            }
        }
        response = self.client.service.FECompConsultar(
            feAuth=self.auth,
            FeCompConsReq=request["FeCompConsReq"]
        )
        comp = response.Resultado.FECmpConsultaResponse
        return {
            "fchProceso": comp.CbteFchProceso,
            "puntoVenta": comp.PtoVta,
            "tipoCbte":   comp.CbteTipo,
            "nroCbte":    comp.CbteNro,
            "estado":     comp.ResultGet,
        }
