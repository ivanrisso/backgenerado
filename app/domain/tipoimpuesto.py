from dataclasses import dataclass
from typing import Optional, List, TYPE_CHECKING
from app.domain.enums import TipoAplicacionEnum, BaseTributarioEnum


if TYPE_CHECKING:
    from app.domain.clienteimpuesto import ClienteImpuesto
    from app.domain.comprobanteimpuesto import ComprobanteImpuesto
    
@dataclass
class TipoImpuesto:
    id: Optional[int]
    codigo_afip: Optional[str]
    nombre: Optional[str]
    descripcion: Optional[str]
    tipo_aplicacion: Optional[TipoAplicacionEnum]
    base_calculo: Optional[BaseTributarioEnum]
    porcentaje: Optional[float]
    editable: Optional[bool]
    obligatorio: Optional[bool]
    activo: Optional[bool]
    clientes: List["ClienteImpuesto"]
    comprobantes: List["ComprobanteImpuesto"]