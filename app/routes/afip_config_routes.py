
from fastapi import APIRouter, Depends, UploadFile, File
from app.core.dependencies import require_roles
from app.services.afip_config_service import AfipConfigService

router = APIRouter(prefix="/config/afip", tags=["Configuracion"])

@router.get("/certs", dependencies=[Depends(require_roles("admin"))])
def get_afip_certs_status():
    """
    Obtiene el estado del certificado AFIP actual.
    """
    return AfipConfigService.get_certificate_info()

@router.post("/certs", dependencies=[Depends(require_roles("admin"))])
async def upload_afip_certs(
    cert_file: UploadFile = File(...),
    key_file: UploadFile = File(...)
):
    """
    Sube nuevos certificado (.crt) y clave privada (.key).
    Sobrescribe los actuales y recarga el cliente AFIP.
    """
    return await AfipConfigService.update_credentials(cert_file, key_file)
