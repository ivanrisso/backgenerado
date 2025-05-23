from typing import Optional, List
from app.domain.enums import TipoAplicacionEnum, BaseTributarioEnum
from pydantic import BaseModel

class TipoImpuesto(BaseModel):
    id: Optional[int]
    codigo_afip: Optional[str]
    nombre: Optional[str]
    descripcion: Optional[str]
    tipo_aplicacion: Optional[TipoAplicacionEnum]
    base_calculo: Optional[BaseTributarioEnum]
    porcentaje: Optional[float]
    editable: Optional[bool]
    obligatorio: Optional[bool]
    activo: Optional[bool]
    
    class Config:
        from_attributes = True
    
    
    