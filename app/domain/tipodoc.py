from dataclasses import dataclass
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.comprobante import Comprobante
    from app.domain.cliente import Cliente
    
@dataclass
class TipoDoc:
    id: Optional[int]
    tipo_doc_nombre: Optional[str]
    habilitado: Optional[bool]
    comprobantes: List["Comprobante"]
    clientes: List["Cliente"]