from typing import Optional
from pydantic import BaseModel

class ClienteImpuesto(BaseModel):
    id: Optional[int]
    cliente_id: Optional[int]
    tipo_impuesto_id: Optional[int]
    aplica: Optional[bool]
    alicuota: Optional[float]
    observaciones: Optional[str]

    class Config:
        from_attributes = True
