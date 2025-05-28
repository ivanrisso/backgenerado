from typing import Optional
from dataclasses import dataclass
from app.domain.entities.enums import TipoAplicacionEnum, BaseTributarioEnum

@dataclass
class TipoImpuesto:
    id: Optional[int] = None
    codigo_afip: Optional[str] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    tipo_aplicacion: Optional[TipoAplicacionEnum] = None
    base_calculo: Optional[BaseTributarioEnum] = None
    porcentaje: Optional[float] = None
    editable: Optional[bool] = None
    obligatorio: Optional[bool] = None
    activo: Optional[bool] = None
    
    
    