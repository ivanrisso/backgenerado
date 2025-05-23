from typing import Optional
from pydantic import BaseModel


class ComprobanteImpuesto(BaseModel):
    id: Optional[int]
    comprobante_id: Optional[int]
    tipo_impuesto_id: Optional[int]
    descripcion: Optional[str]
    base_imponible: Optional[float]
    alicuota: Optional[float]
    importe: Optional[float]

    class Config:
        from_attributes = True
