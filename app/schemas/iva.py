# ✅ app/schemas/iva.py
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class IvaCreate(BaseModel):
    codigo: int
    descripcion: str
    porcentaje: Decimal
    discriminado: bool
    porcentaje_sobre: Decimal

class IvaUpdate(BaseModel):
    codigo: Optional[int] = None
    descripcion: Optional[str] = None
    porcentaje: Optional[Decimal] = None
    discriminado: Optional[bool] = None
    porcentaje_sobre: Optional[Decimal] = None

class IvaResponse(BaseModel):
    id: int 
    codigo: int
    descripcion: str
    porcentaje: Decimal
    discriminado: bool
    porcentaje_sobre: Decimal

    class Config:
        from_attributes = True
        