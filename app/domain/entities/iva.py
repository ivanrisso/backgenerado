from typing import Optional
from decimal import Decimal
from dataclasses import dataclass

@dataclass
class Iva:
    id: Optional[int] = None
    codigo: Optional[int] = None
    descripcion: Optional[str] = None
    porcentaje: Optional[Decimal] = None
    discriminado: Optional[bool] = None
    porcentaje_sobre: Optional[Decimal] = None
