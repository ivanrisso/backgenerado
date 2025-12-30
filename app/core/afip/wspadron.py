
import logging
from zeep import Client, Settings as ZeepSettings
from typing import Dict, Any

logger = logging.getLogger(__name__)

class WSPadronClient:
    WSPADRON_URL_TEST = "https://awshomo.afip.gov.ar/sr-padron/webservices/personaServiceA5?WSDL"
    WSPADRON_URL_PROD = "https://aws.afip.gov.ar/sr-padron/webservices/personaServiceA5?WSDL"

    def __init__(self, wsaa_client, cuit: int, production: bool = False):
        self.wsaa_client = wsaa_client
        self.cuit = cuit
        self.production = production
        self.wsdl = self.WSPADRON_URL_PROD if production else self.WSPADRON_URL_TEST
        self.client = Client(self.wsdl, settings=ZeepSettings(strict=False, xml_huge_tree=True))

    def _get_auth(self):
        # Service name for A5 is usually ws_sr_padron_a5
        token, sign = self.wsaa_client.get_token_and_sign(service="ws_sr_padron_a5")
        return {
            "token": token,
            "sign": sign,
            "idPersona": self.cuit
        }

    def get_persona(self, id_persona: int) -> Dict[str, Any]:
        """
        Retrieves person data from Padron A5.
        """
        auth = self._get_auth()
        
        try:
            # Padron A5 uses 'getPersona' method
            response = self.client.service.getPersona(
                token=auth["token"],
                sign=auth["sign"],
                idPersona=auth["idPersona"],
                idPersonaConsul=id_persona
            )
            
            return response
        except Exception as e:
            logger.error(f"Error getting persona from Padron A5: {e}")
            raise
