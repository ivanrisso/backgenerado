from app.core.config import settings
from .afip.wsaa import WSAAClient
from .afip.wsfe import WSFEClient
from .afip.wspadron import WSPadronClient

import logging
import os

logger = logging.getLogger(__name__)


_wsaa_instance = None
_wsfe_instance = None
_wspadron_instance = None

def _get_wsaa_client() -> WSAAClient:
    global _wsaa_instance
    if _wsaa_instance:
        return _wsaa_instance

    
    # 1. Rutas de certificados
    cert_path = settings.AFIP_CERT_CRT_PATH
    key_path = settings.AFIP_KEY_CRT_PATH

    # Fallback logic because .env might be wrong
    if not os.path.exists(cert_path):
        logger.warning(f"Cert path {cert_path} not found. Trying app/certificado/group.crt")
        if os.path.exists("app/certificado/group.crt"):
            cert_path = "app/certificado/group.crt"
    
    if not os.path.exists(key_path):
        logger.warning(f"Key path {key_path} not found. Trying app/certificado/clave")
        if os.path.exists("app/certificado/clave"):
            key_path = "app/certificado/clave"
            
    logger.info(f"Using Native AFIP Cert: {cert_path}")
    logger.info(f"Using Native AFIP Key: {key_path}")
    import sys
    # Prevent duplicated logs on reload
    if not hasattr(sys, "_afip_cuit_logged"): 
        logger.info(f"Using Native AFIP CUIT: {settings.AFIP_CUIT}")
        sys._afip_cuit_logged = True

    # 2. Inicializar WSAA (Auth)
    _wsaa_instance = WSAAClient(
        key_path=key_path,
        cert_path=cert_path,
        production=settings.AFIP_ENVIRONMENT.lower() == "production"
    )

    return _wsaa_instance

def get_afip_client() -> WSFEClient:
    """
    Returns Singleton WSFEClient (E-billing)
    """
    global _wsfe_instance
    if _wsfe_instance:
        return _wsfe_instance
        
    wsaa = _get_wsaa_client()
    _wsfe_instance = WSFEClient(
        wsaa_client=wsaa,
        cuit=settings.AFIP_CUIT,
        production=settings.AFIP_ENVIRONMENT.lower() == "production"
    )
    return _wsfe_instance

def get_padron_client() -> WSPadronClient:
    """
    Returns Singleton WSPadronClient (A5)
    """
    global _wspadron_instance
    if _wspadron_instance:
        return _wspadron_instance
        
    wsaa = _get_wsaa_client()
    _wspadron_instance = WSPadronClient(
        wsaa_client=wsaa,
        cuit=settings.AFIP_CUIT,
        production=settings.AFIP_ENVIRONMENT.lower() == "production"
    )
    return _wspadron_instance





def reset_afip_clients():
    """
    Resets all singleton instances to force reloading certificates and tokens.
    """
    global _wsaa_instance, _wsfe_instance, _wspadron_instance
    _wsaa_instance = None
    _wsfe_instance = None
    _wspadron_instance = None
    logger.info("AFIP Clients reset. Next request will reload capabilities.")
