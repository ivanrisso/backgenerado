from pydantic import BaseModel
from typing import Optional
from app.domain.entities.enums import TipoAplicacionEnum, BaseTributarioEnum

class TipoImpuestoBase(BaseModel):
    codigo_afip: str
    nombre: str
    descripcion: str
    tipo_aplicacion: TipoAplicacionEnum
    base_calculo: BaseTributarioEnum
    porcentaje: Optional[float]
    editable: bool
    obligatorio: bool
    activo: bool

class TipoImpuestoCreate(BaseModel):
    codigo_afip: str
    nombre: str
    descripcion: str
    tipo_aplicacion: TipoAplicacionEnum
    base_calculo: BaseTributarioEnum
    porcentaje: Optional[float]
    editable: bool
    obligatorio: bool
    activo: bool

class TipoImpuestoUpdate(BaseModel):
    codigo_afip: Optional[str] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    tipo_aplicacion: Optional[TipoAplicacionEnum] = None
    base_calculo: Optional[BaseTributarioEnum] = None
    porcentaje: Optional[float] = None
    editable: Optional[bool] = None
    obligatorio: Optional[bool] = None
    activo: Optional[bool] = None

class TipoImpuestoResponse(TipoImpuestoBase):
    id: int
    codigo_afip: str
    nombre: str
    descripcion: str
    tipo_aplicacion: TipoAplicacionEnum
    base_calculo: BaseTributarioEnum
    porcentaje: Optional[float]
    editable: bool
    obligatorio: bool
    activo: bool

    class Config:
        from_attributes = True
