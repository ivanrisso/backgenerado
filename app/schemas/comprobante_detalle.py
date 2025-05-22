from pydantic import BaseModel

class ComprobanteDetalleBase(BaseModel):
    comprobante_id: int
    iva_id: int
    descripcion: str
    cantidad: float
    precio_unitario: float
    importe: float
    alicuota_iva: float
    importe_iva: float

class ComprobanteDetalleCreate(ComprobanteDetalleBase):
    pass

class ComprobanteDetalleResponse(ComprobanteDetalleBase):
    id: int

    class Config:
        from_attributes = True