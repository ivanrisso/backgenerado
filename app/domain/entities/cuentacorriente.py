from typing import Optional
from datetime import date
from dataclasses import dataclass

@dataclass
class CuentaCorriente:
    id: Optional[int] = None
    cliente_id: Optional[int] = None
    comprobante_id: Optional[int] = None
    fecha: Optional[date] = None
    tipo: Optional[str] = None
    descripcion: Optional[str] = None
    importe: Optional[float] = None
    signo: Optional[int] = None
    saldo: Optional[float] = None
