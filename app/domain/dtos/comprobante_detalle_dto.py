# app/domain/dtos/comprobante_detalle_dto.py
from typing import Optional
from pydantic import BaseModel

class ComprobanteDetalleDTO(BaseModel):
    id: Optional[int] = None
    comprobante_id: Optional[int] = None
    iva_id: Optional[int]
    descripcion: Optional[str]
    cantidad: Optional[float]
    precio_unitario: Optional[float]
    importe: Optional[float]
    alicuota_iva: Optional[float]
    importe_iva: Optional[float]
