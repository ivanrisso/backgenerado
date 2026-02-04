from pydantic import BaseModel
from typing import Optional
from app.domain.entities.enums import TipoPuntoVentaEnum

class PuntoVentaBase(BaseModel):
    numero: int
    tipo: TipoPuntoVentaEnum = TipoPuntoVentaEnum.ELECTRONICA
    bloqueado: bool = False

class PuntoVentaCreate(PuntoVentaBase):
    pass

class PuntoVentaUpdate(BaseModel):
    numero: Optional[int] = None
    tipo: Optional[TipoPuntoVentaEnum] = None
    bloqueado: Optional[bool] = None

class PuntoVentaResponse(PuntoVentaBase):
    id: int

    class Config:
        from_attributes = True
