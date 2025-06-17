# app/core/afip_auth.py

import os, logging, base64
from datetime import datetime, timedelta

from zeep import Client
from zeep.transports import Transport
import requests

from cryptography import x509
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.serialization.pkcs12 import load_key_and_certificates
from cryptography.hazmat.primitives.serialization.pkcs7 import (
    PKCS7SignatureBuilder, PKCS7Options
)

from app.core.config import settings

from afip import Afip

logger = logging.getLogger(__name__)

class AfipAuthService:
    _token: str = None
    _sign: str = None
    _expiry: datetime = None

    def __init__(self):
        # Carga PKCS#12
        p12_path = settings.AFIP_P12_PATH
        p12_pass = settings.AFIP_P12_PASSWORD.encode()
        if not os.path.isfile(p12_path):
            raise RuntimeError(f"PKCS#12 no encontrado: {p12_path}")

        data = open(p12_path, "rb").read()
        private_key, cert, extra_certs = load_key_and_certificates(data, p12_pass)
        self._private_key = private_key
        self._cert = cert
        self._extra_certs = extra_certs or []

        # Prepara sesión con requests_pkcs12
        session = requests.Session()
        from requests_pkcs12 import Pkcs12Adapter
        session.mount(
            "https://",
            Pkcs12Adapter(pkcs12_filename=p12_path, pkcs12_password=p12_pass)
        )
        transport = Transport(session=session, timeout=10)
        self.client = Client(settings.AFIP_WSDL_WSAA, transport=transport)

    def _build_tra(self) -> bytes:
        now = datetime.utcnow()
        uid = int(now.timestamp())
        gen = (now - timedelta(seconds=30)).strftime("%Y-%m-%dT%H:%M:%S-03:00")
        exp = (now + timedelta(minutes=10)).strftime("%Y-%m-%dT%H:%M:%S-03:00")
        xml = f"""<loginTicketRequest version="1.0">
  <header>
    <uniqueId>{uid}</uniqueId>
    <generationTime>{gen}</generationTime>
    <expirationTime>{exp}</expirationTime>
  </header>
  <service>wsfe</service>
</loginTicketRequest>"""
        return xml.encode("utf-8")

    def _sign_tra(self, tra: bytes) -> str:
        """
        Firma el XML TRA como CMS PKCS#7 detached con SHA-256,
        codifica en Base64 y devuelve el string listo para loginCms.
        """
        builder = PKCS7SignatureBuilder() \
            .set_data(tra) \
            .add_signer(
                self._cert,
                self._private_key,
                hashes.SHA256()
            )

        # Firmamos solo como DetachedSignature
        p7_der = builder.sign(
            encoding=serialization.Encoding.DER,
            options=[PKCS7Options.DetachedSignature]
        )

        # Codificamos a Base64 para enviarlo a AFIP
        return base64.b64encode(p7_der).decode("ascii")


    async def get_credentials(self) -> dict:
        now = datetime.utcnow()
        if not self._token or (self._expiry - now) < timedelta(minutes=10):
            logger.info("Renovando token WSAA de AFIP")
            tra = self._build_tra()
            cms_b64 = self._sign_tra(tra)
            resp = self.client.service.loginCms(cms_b64)
            # Extrae directamente de la respuesta de Zeep
            header = resp.loginTicketResponse.header
            creds = resp.loginTicketResponse.credentials
            self._token  = creds.token
            self._sign   = creds.sign
            self._expiry = datetime.fromisoformat(header.expirationTime)
        return {"token": self._token, "sign": self._sign, "cuit": settings.AFIP_CUIT}

    def get_afip_client() -> Afip:
        """
        Devuelve un cliente Afip configurado para WSAA+WSFE.
        Gestiona automáticamente el token/sign internamente.
        """
        return Afip(
            cert_file=settings.AFIP_KEY_CRT_PATH,
            cert_password=settings.AFIP_KEY_CRT_PATH,
            environment=settings.AFIP_ENVIRONMENT.lower(),  # 'production' o 'homologation'
            cuit=settings.AFIP_CUIT
        )