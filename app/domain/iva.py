from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class Iva(BaseModel):
    id: Optional[int] = None
    codigo: Optional[int] = None
    descripcion: Optional[str] = None
    porcentaje: Optional[Decimal] = None
    discriminado: Optional[bool] = None
    porcentaje_sobre: Optional[Decimal] = None

    class Config:
        from_attributes = True
