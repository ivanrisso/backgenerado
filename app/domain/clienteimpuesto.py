from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from app.domain.cliente import Cliente
    from app.domain.tipoimpuesto import TipoImpuesto    

@dataclass
class ClienteImpuesto:
    id: Optional[int]
    cliente_id: Optional[int]
    tipo_impuesto_id: Optional[int]
    aplica: Optional[bool]
    alicuota: Optional[float]
    observaciones: Optional[str]
    cliente: Optional["Cliente"]
    tipo_impuesto: Optional["TipoImpuesto"]