from pydantic import BaseModel
from typing import Optional, Any
from app.domain.entities.enums import AmbitoImpuestoEnum

class CondicionTributariaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    ambito: AmbitoImpuestoEnum = AmbitoImpuestoEnum.NACIONAL
    tipo_impuesto_id: Optional[int] = None

class CondicionTributariaCreate(CondicionTributariaBase):
    pass

class CondicionTributariaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    ambito: Optional[AmbitoImpuestoEnum] = None
    tipo_impuesto_id: Optional[int] = None

class CondicionTributariaResponse(CondicionTributariaBase):
    id: int
    tipo_impuesto: Optional[Any] = None

    class Config:
        from_attributes = True
