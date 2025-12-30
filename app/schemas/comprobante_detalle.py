from pydantic import BaseModel
from typing import Optional

class ComprobanteDetalleCreate(BaseModel):
    comprobante_id: int
    iva_id: int
    descripcion: str
    cantidad: float
    precio_unitario: float
    importe: float
    alicuota_iva: float
    importe_iva: float
    datos_extra: Optional[dict] = None

class ComprobanteDetalleUpdate(BaseModel):
    comprobante_id: Optional[int] = None
    iva_id: Optional[int] = None
    descripcion: Optional[str] = None
    cantidad: Optional[float] = None
    precio_unitario: Optional[float] = None
    importe: Optional[float] = None
    alicuota_iva: Optional[float] = None
    importe_iva: Optional[float] = None
    datos_extra: Optional[dict] = None


class ComprobanteDetalleResponse(BaseModel):
    id: Optional[int]
    comprobante_id: int
    iva_id: int
    descripcion: str
    cantidad: float
    precio_unitario: float
    importe: float
    alicuota_iva: float
    importe_iva: float
    datos_extra: Optional[dict]

    class Config:
        from_attributes = True