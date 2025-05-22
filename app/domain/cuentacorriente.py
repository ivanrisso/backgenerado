from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING
from datetime import date

if TYPE_CHECKING:
    from app.domain.comprobante import Comprobante
    from app.domain.cliente import Cliente


@dataclass
class CuentaCorriente:
    id: Optional[int]
    cliente_id: Optional[int]
    comprobante_id: Optional[int]
    fecha: Optional[date]
    tipo: Optional[str]
    descripcion: Optional[str]
    importe: Optional[float]
    signo: Optional[int]
    saldo: Optional[float]
    cliente: Optional["Cliente"]
    comprobante: Optional["Comprobante"]