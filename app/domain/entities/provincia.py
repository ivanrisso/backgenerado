from typing import Optional
from dataclasses import dataclass

@dataclass
class Provincia:
    id: Optional[int] = None
    provincia_nombre: Optional[str] = None
    pais_id: Optional[int] = None
