from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from app.domain.entities.enums import TipoArticuloEnum
from app.schemas.tipo_impuesto import TipoImpuestoResponse

class ArticuloBase(BaseModel):
    codigo: str
    nombre: str
    descripcion: Optional[str] = None
    precio_venta: float = 0.0
    precio_costo: float = 0.0
    tipo: TipoArticuloEnum = TipoArticuloEnum.SERVICIO
    activo: bool = True
    impuesto_venta_id: Optional[int] = None
    impuesto_compra_id: Optional[int] = None

class ArticuloCreate(ArticuloBase):
    pass

class ArticuloUpdate(BaseModel):
    codigo: Optional[str] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio_venta: Optional[float] = None
    precio_costo: Optional[float] = None
    tipo: Optional[TipoArticuloEnum] = None
    activo: Optional[bool] = None
    impuesto_venta_id: Optional[int] = None
    impuesto_compra_id: Optional[int] = None

class ArticuloResponse(ArticuloBase):
    id: int
    impuesto_venta: Optional[TipoImpuestoResponse] = None
    impuesto_compra: Optional[TipoImpuestoResponse] = None

    model_config = ConfigDict(from_attributes=True)
