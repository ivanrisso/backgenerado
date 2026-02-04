
import os
import shutil
import logging
from datetime import datetime
from fastapi import UploadFile, HTTPException, status
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from app.core.config import settings
from app.core.afip_client import reset_afip_clients

logger = logging.getLogger(__name__)

class AfipConfigService:
    
    @staticmethod
    def get_certificate_info() -> dict:
        cert_path = settings.AFIP_CERT_CRT_PATH
        
        if not os.path.exists(cert_path):
             return {"status": "missing", "path": cert_path}
             
        try:
            with open(cert_path, "rb") as f:
                cert_data = f.read()
                cert = x509.load_pem_x509_certificate(cert_data, default_backend())
                
                valid_from = cert.not_valid_before
                valid_to = cert.not_valid_after
                subject = cert.subject.rfc4514_string()
                issuer = cert.issuer.rfc4514_string()
                
                days_remaining = (valid_to - datetime.utcnow()).days
                
                return {
                    "status": "active",
                    "subject": subject,
                    "issuer": issuer,
                    "valid_from": valid_from.isoformat(),
                    "valid_to": valid_to.isoformat(),
                    "days_remaining": days_remaining,
                    "production": settings.AFIP_ENVIRONMENT.lower() == "production"
                }
        except Exception as e:
            logger.error(f"Error parsing certificate: {e}")
            return {"status": "error", "error": str(e)}

    @staticmethod
    async def update_credentials(cert_file: UploadFile, key_file: UploadFile):
        cert_path = settings.AFIP_CERT_CRT_PATH
        key_path = settings.AFIP_KEY_CRT_PATH
        
        # 1. Validation (Basic)
        if not cert_file.filename.endswith(".crt"):
             raise HTTPException(status.HTTP_400_BAD_REQUEST, "El certificado debe ser .crt")
        if not key_file.filename.endswith(".key"):
             raise HTTPException(status.HTTP_400_BAD_REQUEST, "La clave debe ser .key")
             
        try:
            # 2. Backup existing
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            if os.path.exists(cert_path):
                shutil.copy(cert_path, f"{cert_path}.{timestamp}.bak")
            if os.path.exists(key_path):
                shutil.copy(key_path, f"{key_path}.{timestamp}.bak")
                
            # 3. Save new files
            # Ensure directory exists
            os.makedirs(os.path.dirname(cert_path), exist_ok=True)
            os.makedirs(os.path.dirname(key_path), exist_ok=True)
            
            with open(cert_path, "wb") as buffer:
                shutil.copyfileobj(cert_file.file, buffer)
                
            with open(key_path, "wb") as buffer:
                shutil.copyfileobj(key_file.file, buffer)
            
            # 3.1 Secure permissions (Owner read/write only)
            os.chmod(key_path, 0o600)
                
            # 4. Reset Clients
            reset_afip_clients()
            
            return {"message": "Credenciales actualizadas correctamente. El sistema recargará la conexión en la próxima solicitud."}
            
        except Exception as e:
            logger.error(f"Error updating credentials: {e}")
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Error actualizando credenciales: {e}")
