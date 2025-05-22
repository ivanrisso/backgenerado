from dataclasses import dataclass
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.telefono import Telefono

@dataclass
class TipoTel:
    id: Optional[int]
    nombre: Optional[str]
    telefonos: List["Telefono"]