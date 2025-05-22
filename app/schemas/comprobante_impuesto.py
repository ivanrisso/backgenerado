from pydantic import BaseModel

class ComprobanteImpuestoBase(BaseModel):
    comprobante_id: int
    tipo_impuesto_id: int
    descripcion: str
    base_imponible: float
    alicuota: float
    importe: float

class ComprobanteImpuestoCreate(ComprobanteImpuestoBase):
    pass

class ComprobanteImpuestoResponse(ComprobanteImpuestoBase):
    id: int

    class Config:
        from_attributes = True