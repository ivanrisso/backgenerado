from dataclasses import dataclass
from typing import Optional

@dataclass
class CondicionIva:
    id: Optional[int] = None
    codigo: int = 0
    descripcion: str = ""
