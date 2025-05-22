from dataclasses import dataclass
from typing import Optional, List, TYPE_CHECKING
from decimal import Decimal

if TYPE_CHECKING:
    from app.domain.comprobante import Comprobante
    from app.domain.iva import Iva


@dataclass
class ComprobanteDetalle:
    id: Optional[int]
    comprobante_id: Optional[int]
    iva_id: Optional[int]
    descripcion: Optional[str]
    cantidad: Optional[float]
    precio_unitario: Optional[float]
    importe: Optional[float]
    alicuota_iva: Optional[float]
    importe_iva: Optional[float]
    comprobante: Optional["Comprobante"]
    iva: Optional["Iva"]