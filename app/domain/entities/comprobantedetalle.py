from typing import Optional
from dataclasses import dataclass

@dataclass
class ComprobanteDetalle:
    id: Optional[int] = None
    comprobante_id: Optional[int] = None
    iva_id: Optional[int] = None
    descripcion: Optional[str] = None
    cantidad: Optional[float] = None
    precio_unitario: Optional[float] = None
    importe: Optional[float] = None
    alicuota_iva: Optional[float] = None
    importe_iva: Optional[float] = None
    
