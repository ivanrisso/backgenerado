from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING
from datetime import date, datetime
from app.domain.usuario import Usuario


if TYPE_CHECKING:
    from app.domain.comprobante import Comprobante

@dataclass
class AuditoriaComprobante:
    id: Optional[int]
    comprobante_id: Optional[int]
    usuario_id: Optional[int]
    accion: Optional[str]
    detalle: Optional[str]
    ip_origen: Optional[str]
    fecha: Optional[datetime]
    comprobante: Optional["Comprobante"]
    usuario: Optional[Usuario]