from typing import Optional
from dataclasses import dataclass

@dataclass
class Domicilio:
    id: Optional[int] = None
    calle: Optional[str] = None
    numero: Optional[int] = None
    cliente_id: Optional[int] = None
    tipo_dom_id: Optional[int] = None
    localidad_id: Optional[int] = None
