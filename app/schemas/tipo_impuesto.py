from pydantic import BaseModel
from typing import Optional
from app.domain.enums import TipoAplicacionEnum, BaseTributarioEnum

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

class TipoImpuestoCreate(TipoImpuestoBase):
    pass

class TipoImpuestoResponse(TipoImpuestoBase):
    id: int

    class Config:
        from_attributes = True
