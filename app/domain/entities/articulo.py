from dataclasses import dataclass, field
from typing import Optional
from app.domain.entities.enums import TipoArticuloEnum
from app.domain.entities.tipoimpuesto import TipoImpuesto

@dataclass
class Articulo:
    id: Optional[int] = None
    codigo: str = ""
    nombre: str = ""
    descripcion: Optional[str] = None
    precio_venta: float = 0.0
    precio_costo: float = 0.0
    tipo: TipoArticuloEnum = TipoArticuloEnum.SERVICIO
    activo: bool = True
    
    impuesto_venta_id: Optional[int] = None
    impuesto_compra_id: Optional[int] = None
    
    # Optional related entities
    impuesto_venta: Optional[TipoImpuesto] = None
    impuesto_compra: Optional[TipoImpuesto] = None
