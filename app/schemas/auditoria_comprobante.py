from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AuditoriaComprobanteCreate(BaseModel):
    comprobante_id: int
    usuario_id: int
    accion: str
    detalle: Optional[str]
    ip_origen: Optional[str]
    fecha: datetime

# Para creación desde el cliente (sin ID ni fecha)
class AuditoriaComprobanteUpdate(BaseModel):
    comprobante_id: Optional[int] = None
    usuario_id: Optional[int] = None
    accion: Optional[str] = None
    detalle: Optional[str] = None
    ip_origen: Optional[str] = None
    fecha: Optional[datetime] = None

class AuditoriaComprobanteResponse(BaseModel):
    id: int
    comprobante_id: int
    usuario_id: int
    accion: str
    detalle: str
    ip_origen: str
    fecha: datetime

    class Config:
        from_attributes = True