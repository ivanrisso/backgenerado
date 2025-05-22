from dataclasses import dataclass
from typing import Optional, List
from decimal import Decimal
from datetime import date, datetime

@dataclass
class Concepto:
    id: Optional[int]
    codigo: Optional[str]
    descripcion: Optional[str]
    comprobantes: List["Comprobante"]