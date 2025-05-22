from dataclasses import dataclass
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.provincia import Provincia


@dataclass
class Pais:
    id: Optional[int]
    codigo: Optional[str]
    nombre: Optional[str]
    provincias: List["Provincia"]