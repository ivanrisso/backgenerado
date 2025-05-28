from typing import Optional
from dataclasses import dataclass

@dataclass
class ComprobanteImpuesto:
    id: Optional[int] = None
    comprobante_id: Optional[int] = None
    tipo_impuesto_id: Optional[int] = None
    descripcion: Optional[str] = None
    base_imponible: Optional[float] = None
    alicuota: Optional[float] = None
    importe: Optional[float] = None

