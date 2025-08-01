from typing import Optional
from dataclasses import dataclass

@dataclass
class Moneda:
    id: Optional[int] = None
    codigo: Optional[str] = None
    descripcion: Optional[str] = None
    codigo_arca: Optional[str] = None