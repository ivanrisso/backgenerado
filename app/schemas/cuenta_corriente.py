from pydantic import BaseModel
from typing import Optional
from datetime import date

class CuentaCorrienteCreate(BaseModel):
    cliente_id: int
    comprobante_id: int
    fecha: date
    tipo: str
    descripcion: str
    importe: float
    signo: int
    saldo: float

class CuentaCorrienteUpdate(BaseModel):
    cliente_id: Optional[int] = None
    comprobante_id: Optional[int] = None
    fecha: Optional[date] = None
    tipo: Optional[str] = None
    descripcion: Optional[str] = None
    importe: Optional[float] = None
    signo: Optional[int] = None
    saldo: Optional[float] = None

class CuentaCorrienteResponse(BaseModel):
    id: int
    cliente_id: int
    comprobante_id: int
    fecha: date
    tipo: str
    descripcion: str
    importe: float
    signo: int
    saldo: float

    class Config:
        from_attributes = True
