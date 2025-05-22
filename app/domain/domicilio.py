from dataclasses import dataclass
from typing import Optional, List, TYPE_CHECKING
from app.domain.tipodom import TipoDom
from app.domain.localidad import Localidad
from app.domain.telefono import Telefono

if TYPE_CHECKING:
    from app.domain.cliente import Cliente

@dataclass
class Domicilio:
    id: Optional[int]
    calle: Optional[str]
    numero: Optional[int]
    cliente_id: Optional[int]
    tipo_dom_id: Optional[int]
    localidad_id: Optional[int]
    cliente: Optional["Cliente"]
    tipo_dom: Optional[TipoDom]
    localidad: Optional[Localidad]
    telefonos: List["Telefono"]