from typing import Optional
from dataclasses import dataclass

@dataclass
class Localidad:
    id: Optional[int] = None
    localidad_nombre: Optional[str] = None
    cod_postal: Optional[str] = None
    provincia_id: Optional[int] = None
    