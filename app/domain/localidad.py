from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING, List

if TYPE_CHECKING:
    from app.domain.provincia import Provincia
    from app.domain.domicilio import Domicilio


@dataclass
class Localidad:
    id: Optional[int]
    localidad_nombre: Optional[str]
    cod_postal: Optional[str]
    provincia_id: Optional[int]
    provincia: Optional["Provincia"]
    domicilios: List["Domicilio"]