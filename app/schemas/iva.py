from pydantic import BaseModel
from decimal import Decimal

class IvaBase(BaseModel):
    codigo: int
    descripcion: str
    porcentaje: Decimal
    discriminado: bool
    porcentaje_sobre: Decimal

class IvaCreate(IvaBase):
    pass

class IvaResponse(IvaBase):
    id: int

    class Config:
        from_attributes = True
        