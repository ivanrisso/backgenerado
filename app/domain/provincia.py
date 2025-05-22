from dataclasses import dataclass
from typing import Optional, List, TYPE_CHECKING


if TYPE_CHECKING:
    from app.domain.pais import Pais
    from app.domain.localidad import Localidad

@dataclass
class Provincia:
    id: Optional[int]
    provincia_nombre: Optional[str]
    pais_id: Optional[int]
    pais: Optional["Pais"]
    localidades: List["Localidad"]