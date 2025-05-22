from dataclasses import dataclass
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.domicilio import Domicilio


@dataclass
class TipoDom:
    id: Optional[int]
    nombre: Optional[str]
    domicilios: List["Domicilio"]