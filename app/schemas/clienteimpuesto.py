from pydantic import BaseModel
from typing import Optional


class ClienteImpuestoBase(BaseModel):
    cliente_id: Optional[int]
    tipo_impuesto_id: Optional[int]
    aplica: Optional[bool] = True
    alicuota: Optional[float] = None
    observaciones: Optional[str] = None


class ClienteImpuestoCreate(ClienteImpuestoBase):
    pass


class ClienteImpuestoResponse(ClienteImpuestoBase):
    id: int

    class Config:
        from_attributes = True
