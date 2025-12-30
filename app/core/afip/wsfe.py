
import logging
from zeep import Client, Settings as ZeepSettings
from typing import Dict, Any

logger = logging.getLogger(__name__)

class WSFEClient:
    WSFE_URL_TEST = "https://wswhomo.afip.gov.ar/wsfev1/service.asmx?WSDL"
    WSFE_URL_PROD = "https://servicios1.afip.gov.ar/wsfev1/service.asmx?WSDL"

    def __init__(self, wsaa_client, cuit: int, production: bool = False):
        self.wsaa_client = wsaa_client
        self.cuit = cuit
        self.production = production
        self.wsdl = self.WSFE_URL_PROD if production else self.WSFE_URL_TEST
        self.client = Client(self.wsdl, settings=ZeepSettings(strict=False, xml_huge_tree=True))

    def _get_auth(self):
        token, sign = self.wsaa_client.get_token_and_sign()
        return {
            "Token": token,
            "Sign": sign,
            "Cuit": self.cuit
        }

    def get_last_voucher(self, punto_venta: int, tipo_comprobante: int) -> int:
        """
        Retorna el último número de comprobante autorizado para un punto de venta y tipo.
        """
        auth = self._get_auth()
        
        try:
            response = self.client.service.FECompUltimoAutorizado(
                Auth=auth,
                PtoVta=punto_venta,
                CbteTipo=tipo_comprobante
            )
            
            if response.Errors:
                err_msg = "; ".join([f"{e.Code}: {e.Msg}" for e in response.Errors.Err])
                raise Exception(f"FECompUltimoAutorizado Error: {err_msg}")
                
            return response.CbteNro
        except Exception as e:
            logger.error(f"Error getting last voucher: {e}")
            raise

    def create_voucher(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Solicita CAE (FECAESolicitar).
        Expects 'data' to be a dict matching FeCAEReq structure roughly, 
        but we need to adapt it to Zeep's expected input.
        """
        auth = self._get_auth()
        
        # Zeep expects the arguments as defined in WSDL
        # FECAESolicitar(Auth, FeCAEReq)
        
        # FeCAEReq structure:
        # {
        #   "FeCabReq": { "CantReg": 1, "PtoVta": ..., "CbteTipo": ... },
        #   "FeDetReq": { "FECAEDetRequest": [ ... ] }
        # }
        
        # We assume 'data' contains ready-to-use FeCabReq and FeDetReq or we build it here?
        # The AfipAdapter constructs a payload. Ideally we pass that payload mostly as is.
        # But `afip-py` had its own structure. We need to match Zeep structure.
        
        req = {
            "FeCabReq": {
                "CantReg": 1,
                "PtoVta": data["FeCabReq"]["PtoVta"],
                "CbteTipo": data["FeCabReq"]["CbteTipo"]
            },
            "FeDetReq": {
                "FECAEDetRequest": [
                    # ... Map details ...
                    data["FeDetReq"][0] # Assume single voucher for now
                ]
            }
        }
        
        try:
            response = self.client.service.FECAESolicitar(
                Auth=auth,
                FeCAEReq=req
            )
            
            # Check for Errors
            if response.Errors:
                 err_msg = "; ".join([f"{e.Code}: {e.Msg}" for e in response.Errors.Err])
                 raise Exception(f"FECAESolicitar Error: {err_msg}")
            
            # Check for Observations in the first detail result
            # response.FeDetResp.FECAEDetResponse[0].Observaciones
            
            # Return full response or just the CAE part?
            # AfipAdapter expects a dict with similar structure to what `afip-py` returned.
            
            return response
            
        except Exception as e:
            logger.error(f"Error creating voucher: {e}")
            raise
