from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AuditoriaComprobanteBase(BaseModel):
    comprobante_id: int
    usuario_id: int
    accion: str
    detalle: Optional[str]
    ip_origen: Optional[str]
    fecha: datetime

# Para creación desde el cliente (sin ID ni fecha)
class AuditoriaComprobanteCreate(AuditoriaComprobanteBase):
    pass

class AuditoriaComprobanteResponse(AuditoriaComprobanteBase):
    id: int

    class Config:
        from_attributes = True