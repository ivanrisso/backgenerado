from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from app.domain.cliente import Cliente

@dataclass
class Operador:
    id: Optional[int]
    cliente_id: Optional[int]
    cliente: Optional["Cliente"]