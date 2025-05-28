from typing import Optional
from dataclasses import dataclass

@dataclass
class Pais:
    id: Optional[int] = None
    codigo: Optional[str] = None 
    nombre: Optional[str] = None
