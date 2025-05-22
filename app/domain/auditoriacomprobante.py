from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AuditoriaComprobante(BaseModel):
    id: Optional[int]
    comprobante_id: Optional[int]
    usuario_id: Optional[int]
    accion: Optional[str]
    detalle: Optional[str]
    ip_origen: Optional[str]
    fecha: Optional[datetime]

    class Config:
        from_attributes = True
