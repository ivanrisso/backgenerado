from pydantic import BaseModel
from typing import Optional


class ClienteImpuestoCreate(BaseModel):
    cliente_id: int
    tipo_impuesto_id: int
    aplica: bool = True
    alicuota: float
    observaciones: str


class ClienteImpuestoUpdate(BaseModel):
    cliente_id: Optional[int] = None
    tipo_impuesto_id: Optional[int] = None
    aplica: Optional[bool] = None
    alicuota: Optional[float] = None
    observaciones: Optional[str] = None


class ClienteImpuestoResponse(BaseModel):
    id: int
    cliente_id: int
    tipo_impuesto_id: int
    aplica: bool
    alicuota: float
    observaciones: str

    class Config:
        from_attributes = True
