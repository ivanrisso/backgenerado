# app/core/afip_client.py

from afip import Afip
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def get_afip_client() -> Afip:
    """
    Instancia el cliente Afip SDK con un dict de opciones:
      - CUIT: tu CUIT
      - production: True/False según entorno
      - cert: ruta al PEM (o .p12 convertido a PEM)
      - key: ruta a la clave privada PEM
      - access_token: None -> se generará internamente
    """
    # Si estás usando .p12, primero conviértelo a PEM con openssl:
    # openssl pkcs12 -in afip.p12 -clcerts -nokeys -out certificado.pem
    # openssl pkcs12 -in afip.p12 -nocerts -out clave.pem -nodes

   # 1. Leer el PEM del certificado
    with open(settings.AFIP_CERT_CRT_PATH, "r") as f:
        cert_pem = f.read()
    # 2. Leer el PEM de la clave
    with open(settings.AFIP_KEY_CRT_PATH, "r") as f:
        key_pem = f.read()


    return Afip({
        "CUIT": settings.AFIP_CUIT,
        "production": settings.AFIP_ENVIRONMENT.lower() == "production",
        "cert": cert_pem, #settings.AFIP_CERT_CRT_PATH,  # define en settings
        "key":  key_pem, #settings.AFIP_KEY_CRT_PATH,   # define en settings
        "access_token": None
    })




