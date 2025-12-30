
from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass
class Imputacion:
    id: Optional[int]
    comprobante_credito_id: int
    comprobante_debito_id: int
    importe: float
    fecha: date
