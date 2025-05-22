from pydantic import BaseModel
from typing import Optional
from datetime import date

class CuentaCorrienteBase(BaseModel):
    cliente_id: int
    comprobante_id: Optional[int]
    fecha: date
    tipo: str
    descripcion: Optional[str] = None
    importe: float
    signo: int
    saldo: Optional[float] = None

class CuentaCorrienteCreate(CuentaCorrienteBase):
    pass

class CuentaCorrienteResponse(CuentaCorrienteBase):
    id: int

    class Config:
        from_attributes = True
