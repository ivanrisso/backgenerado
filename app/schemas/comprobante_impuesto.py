from pydantic import BaseModel
from typing import Optional

class ComprobanteImpuestoCreate(BaseModel):
    comprobante_id: int
    tipo_impuesto_id: int
    descripcion: str
    base_imponible: float
    alicuota: float
    importe: float

class ComprobanteImpuestoUpdate(BaseModel):
    comprobante_id: Optional[int] = None
    tipo_impuesto_id: Optional[int] = None
    descripcion: Optional[str] = None
    base_imponible: Optional[float] = None
    alicuota: Optional[float] = None
    importe: Optional[float] = None

class ComprobanteImpuestoResponse(BaseModel):
    id: Optional[int]
    comprobante_id: int
    tipo_impuesto_id: int
    descripcion: str
    base_imponible: float
    alicuota: float
    importe: float

    class Config:
        from_attributes = True