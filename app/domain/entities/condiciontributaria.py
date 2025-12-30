from typing import Optional, Any
from dataclasses import dataclass
from app.domain.entities.enums import AmbitoImpuestoEnum

@dataclass
class CondicionTributaria:
    id: Optional[int] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    ambito: Optional[AmbitoImpuestoEnum] = None
    tipo_impuesto_id: Optional[int] = None
    tipo_impuesto: Optional[Any] = None
