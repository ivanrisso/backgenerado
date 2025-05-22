from dataclasses import dataclass
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.comprobante import Comprobante
    
@dataclass
class TipoComprobante:
    id: Optional[int]
    codigo: Optional[str]
    descripcion: Optional[str]
    es_fiscal: Optional[bool]
    comprobantes: List["Comprobante"]