
import logging
import time
import email
from datetime import datetime, timedelta
from typing import Tuple

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.serialization import pkcs7
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.primitives.asymmetric import rsa

import requests
from zeep import Client

logger = logging.getLogger(__name__)

class WSAAClient:
    # URL de Producción y Homologación
    WSAA_URL_TEST = "https://wsaahomo.afip.gov.ar/ws/services/LoginCms?wsdl"
    WSAA_URL_PROD = "https://wsaa.afip.gov.ar/ws/services/LoginCms?wsdl"

    def __init__(self, key_path: str, cert_path: str, production: bool = False):
        self.key_path = key_path
        self.cert_path = cert_path
        self.production = production
        self.wsdl = self.WSAA_URL_PROD if production else self.WSAA_URL_TEST
        self.service = "wsfe" # Default service
        
        # Cache for Token/Sign per service
        self._tokens = {} # { service_name: token }
        self._signs = {}  # { service_name: sign }
        self._expirations = {} # { service_name: expiration_dt }

        
        import os
        self.CACHE_FILE = "afip_token_cache.json"

    def get_token_and_sign(self, service: str = "wsfe") -> Tuple[str, str]:
        """
        Devuelve (Token, Sign) válidos para el servicio solicitado. Si expiraron, genera nuevos.
        Checks file cache first.
        """
        
        # 1. Try to load from memory or file if not already in memory
        if service not in self._tokens:
             self._load_from_cache(service)
             
        # 2. Validate expiration
        token = self._tokens.get(service)
        sign = self._signs.get(service)
        expiration = self._expirations.get(service)

        if token and sign and expiration:
            # Buffer of 2 minutes
            if datetime.now().astimezone() < (expiration - timedelta(minutes=2)):
                 return token, sign
            else:
                 logger.info(f"Token para {service} expirado o próximo a expirar.")

        logger.info(f"Generando nuevo Token/Sign en AFIP WSAA para servicio: {service}")
        try:
            tra = self._create_tra(service)
            cms = self._sign_tra(tra)
            token, sign, expiration_time = self._call_wsaa(cms)
            
            self._tokens[service] = token
            self._signs[service] = sign
            self._expirations[service] = expiration_time
            
            self._save_to_cache(service)
            
            return token, sign

        except Exception as e:
            logger.error(f"Error en autenticación AFIP WSAA: {e}")
            raise
            
    def _load_from_cache(self, service: str):
        import json
        import os
        cache_file = f"afip_token_cache_{service}.json"
        if os.path.exists(cache_file):
             try:
                 with open(cache_file, "r") as f:
                     data = json.load(f)
                     exp = datetime.fromisoformat(data["expiration"])
                     
                     self._tokens[service] = data["token"]
                     self._signs[service] = data["sign"]
                     self._expirations[service] = exp
                     logger.info(f"Token AFIP para {service} cargado desde caché local")
             except Exception as e:
                 logger.warning(f"Error cargando caché AFIP para {service}: {e}")
    
    def _save_to_cache(self, service: str):
        import json
        try:
            cache_file = f"afip_token_cache_{service}.json"
            data = {
                "token": self._tokens[service],
                "sign": self._signs[service],
                "expiration": self._expirations[service].isoformat()
            }
            with open(cache_file, "w") as f:
                json.dump(data, f)
            logger.info(f"Token AFIP para {service} guardado en caché local")
        except Exception as e:
            logger.warning(f"Error guardando caché AFIP para {service}: {e}")

    def _create_tra(self, service: str) -> str:

        unique_id = int(time.time())
        # Subtract 10 minutes to avoid any "future time" issues due to clock skew
        generated_time = datetime.now() - timedelta(minutes=10)
        expiration_time = generated_time + timedelta(minutes=20) # Valid for 20 mins from gen time
        
        # Format XML dates: YYYY-MM-DDThh:mm:ss-03:00 (Hardcoded ART)
        fmt = "%Y-%m-%dT%H:%M:%S"
        
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<loginTicketRequest version="1.0">
  <header>
    <uniqueId>{unique_id}</uniqueId>
    <generationTime>{generated_time.strftime(fmt)}-03:00</generationTime>
    <expirationTime>{expiration_time.strftime(fmt)}-03:00</expirationTime>
  </header>
  <service>{service}</service>
</loginTicketRequest>"""

        return xml

    def _sign_tra(self, tra_xml: str) -> str:
        # Load Key
        with open(self.key_path, "rb") as f:
            key_data = f.read()
            private_key = serialization.load_pem_private_key(key_data, password=None)

        # Load Cert
        with open(self.cert_path, "rb") as f:
            cert_data = f.read()
            cert = load_pem_x509_certificate(cert_data)

        # Sign using PKCS7 (CMS)
        # Cryptography doesn't have a high-level CMS sign builder for specific CMS structures easily
        # Wait, cryptography DOES expose PKCS7 signing via serialization since extremely recent versions?
        # Actually, standard `cryptography` might allow creating CMS if compiled with openssl.
        # However, many python implementations open a subprocess to openssl because python libs are tricky with CMS.
        # But we want to avoid subprocess "openssl" dependency if possible (though likely installed).
        # Let's try `subprocess` with openssl if `cryptography` is too low level.
        # BUT, `requests-pkcs12` or similar might be installed?
        # I checked imports.
        
        # Simpler approach: Use `openssl` command line if available. It's standard on linux.
        # Python `cryptography` doesn't fully support PKCS7 generation yet (only loading).
        # Wait, newer versions might.
        # Let's fallback to `openssl` subprocess which is robust and standard for this.
        
        import subprocess
        import tempfile
        
        with tempfile.NamedTemporaryFile("w") as xml_file:
            xml_file.write(tra_xml)
            xml_file.flush()
            
            # openssl smime -sign -in TRA.xml -out TRA.tmp -signer cert -inkey key -outform PEM -nodetach
            # -nodetach is critical for AFIP
            
            cmd = [
                "openssl", "smime", "-sign",
                "-in", xml_file.name,
                "-signer", self.cert_path,
                "-inkey", self.key_path,
                "-outform", "PEM",
                "-nodetach"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                 raise Exception(f"OpenSSL Error: {result.stderr}")
            
            # The output is the CMS
            # We need to remove the headers usually (MIME headers) -> AFIP expects purely the base64 content?
            # Or the full PEM?
            # AFIP LoginCms expects the PEM content string (including headers sometimes, or purely the DER base64).
            # Usually strict PEM format works.
            
            # However, `smime -sign` adds "Content-Type: application/x-pkcs7-mime; name=smime.p7m" headers.
            # We need to strip those headers to get just the PEM block or just extracting the CMS.
            # Actually, `openssl cms` is preferred if available, but `smime` is ubiquitous.
            
            cms_pem = result.stdout
            
            # Strip MIME headers and PEM headers -> Return only the Base64 content
            lines = cms_pem.splitlines()
            cms_clean = []
            in_block = False
            for line in lines:
                if "BEGIN PKCS7" in line:
                    in_block = True
                    continue # Skip start line
                if "END PKCS7" in line:
                    in_block = False
                    continue # Skip end line
                
                if in_block and line.strip(): # Add only content lines
                    cms_clean.append(line.strip())
                    
            return "".join(cms_clean)


    def _call_wsaa(self, cms: str) -> Tuple[str, str, datetime]:
        client = Client(self.wsdl)
        
        # Zeep automatically parses the WSDL
        response = client.service.loginCms(in0=cms)
        
        # Parse result: loginTicketResponse
        # It's an XML string inside the response usually
        import xml.etree.ElementTree as ET
        
        root = ET.fromstring(response)
        # Structure: <loginTicketResponse><header>...</header><credentials><token>...</token><sign>...</sign></credentials></loginTicketResponse>
        
        token = root.find(".//token").text
        sign = root.find(".//sign").text
        exp_time_str = root.find(".//expirationTime").text # 2025-12-27T19:25:24.000-03:00
        
        # Clean TZ? 
        # python isoformat parsing in recent versions handles it well
        # But let's be safe.
        # AFIP returns with timezone.
        
        # If python < 3.11, fromisoformat might struggle with some TZ formats?
        # Let's assume 3.10+ (which is used here).
        expiration = datetime.fromisoformat(exp_time_str)
        
        return token, sign, expiration
