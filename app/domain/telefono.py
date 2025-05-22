from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.tipotel import TipoTel
    from app.domain.domicilio import Domicilio

@dataclass
class Telefono:
    id: Optional[int]
    tipo_tel_id: Optional[int]
    prefijo: Optional[str]
    numero: Optional[str]
    domicilio_id: Optional[int]
    tipo_tel: Optional["TipoTel"]
    domicilio: Optional["Domicilio"]