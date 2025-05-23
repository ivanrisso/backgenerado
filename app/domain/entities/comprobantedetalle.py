from typing import Optional
from pydantic import BaseModel

class ComprobanteDetalle(BaseModel):
    id: Optional[int]
    comprobante_id: Optional[int]
    iva_id: Optional[int]
    descripcion: Optional[str]
    cantidad: Optional[float]
    precio_unitario: Optional[float]
    importe: Optional[float]
    alicuota_iva: Optional[float]
    importe_iva: Optional[float]
    
    class Config:
        from_attributes = True
