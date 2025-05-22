from dataclasses import dataclass
from typing import Optional, List, TYPE_CHECKING


if TYPE_CHECKING:
    from app.domain.comprobante import Comprobante
    from app.domain.tipoimpuesto import TipoImpuesto    

@dataclass
class ComprobanteImpuesto:
    id: Optional[int]
    comprobante_id: Optional[int]
    tipo_impuesto_id: Optional[int]
    descripcion: Optional[str]
    base_imponible: Optional[float]
    alicuota: Optional[float]
    importe: Optional[float]
    comprobante: Optional["Comprobante"]
    tipo_impuesto: Optional["TipoImpuesto"]