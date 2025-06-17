# src/infrastructure/clients/wsaa_client.py
import os
from zeep import Client
from OpenSSL import crypto
from typing import Tuple
from datetime import datetime, timedelta
import tempfile

class WsaaClient:
    def __init__(self):
        self.wsdl = os.getenv("WSAA_WSDL")
        self.cert_path = os.getenv("CERT_PATH")
        self.key_path = os.getenv("KEY_PATH")
        self.cuit = os.getenv("CUIT")
        self.client = Client(self.wsdl)

    def _build_cms(self) -> str:
        """
        Genera un CMS PKCS#7 firmado con tu certificado y clave privada.
        """
        # Cargar certificado y clave
        cert = crypto.load_certificate(crypto.FILETYPE_PEM, open(self.cert_path).read())
        key  = crypto.load_privatekey(crypto.FILETYPE_PEM, open(self.key_path).read())

        # Crear estructura PKCS#7
        pkcs7 = crypto.PKCS7_sign(
            cert, key, [], crypto.PKCS7_BINARY | crypto.PKCS7_DETACHED
        )

        # Exportar CMS en DER y luego base64
        der = crypto.dump_pkcs7(pkcs7)
        return der.encode("base64")

    def obtener_ticket(self) -> Tuple[str, str]:
        """
        Llama al servicio LoginCms de AFIP y retorna (token, sign).
        """
        cms = self._build_cms()
        response = self.client.service.LoginCms(in0=cms)
        # El resultado viene en un XML con <token> y <sign>
        # Zeep nos entrega response.result como string XML
        from xml.etree import ElementTree as ET
        root = ET.fromstring(response.result)
        token = root.findtext(".//token")
        sign  = root.findtext(".//sign")
        return token, sign
