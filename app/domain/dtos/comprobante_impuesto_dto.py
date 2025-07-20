# app/domain/dtos/comprobante_impuesto_dto.py
from typing import Optional
from pydantic import BaseModel

class ComprobanteImpuestoDTO(BaseModel):
    id: Optional[int] = None
    comprobante_id: Optional[int] = None
    tipo_impuesto_id: Optional[int]
    descripcion: Optional[str]
    base_imponible: Optional[float]
    alicuota: Optional[float]
    importe: Optional[float]
