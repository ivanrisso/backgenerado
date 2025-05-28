from typing import Optional
from datetime import datetime
from dataclasses import dataclass

@dataclass
class AuditoriaComprobante:
    id: Optional[int] = None
    comprobante_id: Optional[int] = None
    usuario_id: Optional[int] = None
    accion: Optional[str] = None
    detalle: Optional[str] = None
    ip_origen: Optional[str] = None
    fecha: Optional[datetime] = None
