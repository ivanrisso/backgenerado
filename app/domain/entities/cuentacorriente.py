from typing import Optional
from datetime import date
from pydantic import BaseModel

class CuentaCorriente(BaseModel):
    id: Optional[int]
    cliente_id: Optional[int]
    comprobante_id: Optional[int]
    fecha: Optional[date]
    tipo: Optional[str]
    descripcion: Optional[str]
    importe: Optional[float]
    signo: Optional[int]
    saldo: Optional[float]

    class Config:
        from_attributes = True
