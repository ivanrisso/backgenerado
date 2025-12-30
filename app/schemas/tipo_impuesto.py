from pydantic import BaseModel
from typing import Optional, List
from app.domain.entities.enums import (
    TipoAplicacionEnum, BaseTributarioEnum, AmbitoImpuestoEnum, 
    CategoriaImpuestoEnum, TipoUsoImpuestoEnum, MetodoCalculoImpuestoEnum,
    AmbitoUsoImpuestoEnum, CategoriaFiscalImpuestoEnum
)
from app.schemas.condicion_tributaria import CondicionTributariaResponse

class TipoImpuestoBase(BaseModel):
    codigo_afip: str
    nombre: str
    descripcion: str
    tipo_aplicacion: TipoAplicacionEnum
    base_calculo: BaseTributarioEnum
    ambito: AmbitoImpuestoEnum = AmbitoImpuestoEnum.NACIONAL
    categoria: CategoriaImpuestoEnum = CategoriaImpuestoEnum.IMPUESTO_DIRECTO
    porcentaje: Optional[float]
    editable: bool
    obligatorio: bool
    activo: bool
    
    # Odoo fields
    tipo_uso: TipoUsoImpuestoEnum = TipoUsoImpuestoEnum.VENTAS
    metodo_calculo: MetodoCalculoImpuestoEnum = MetodoCalculoImpuestoEnum.PORCENTAJE
    ambito_uso: AmbitoUsoImpuestoEnum = AmbitoUsoImpuestoEnum.AMBOS
    importe: float = 0.0
    etiqueta_factura: Optional[str] = None
    incluido_precio: bool = False
    afecta_base_subsecuente: bool = False
    categoria_fiscal: Optional[CategoriaFiscalImpuestoEnum] = None
    notas_legales: Optional[str] = None
    cuenta_impuesto_vta: Optional[str] = None
    cuenta_impuesto_com: Optional[str] = None

from app.schemas.tipo_impuesto_distribucion import TipoImpuestoDistribucionCreate, TipoImpuestoDistribucionResponse

class TipoImpuestoCreate(TipoImpuestoBase):
    reparticiones: Optional[List[TipoImpuestoDistribucionCreate]] = None

class TipoImpuestoUpdate(BaseModel):
    codigo_afip: Optional[str] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    tipo_aplicacion: Optional[TipoAplicacionEnum] = None
    base_calculo: Optional[BaseTributarioEnum] = None
    ambito: Optional[AmbitoImpuestoEnum] = None
    categoria: Optional[CategoriaImpuestoEnum] = None
    porcentaje: Optional[float] = None
    editable: Optional[bool] = None
    obligatorio: Optional[bool] = None
    activo: Optional[bool] = None
    
    # Odoo fields
    tipo_uso: Optional[TipoUsoImpuestoEnum] = None
    metodo_calculo: Optional[MetodoCalculoImpuestoEnum] = None
    ambito_uso: Optional[AmbitoUsoImpuestoEnum] = None
    importe: Optional[float] = None
    etiqueta_factura: Optional[str] = None
    incluido_precio: Optional[bool] = None
    afecta_base_subsecuente: Optional[bool] = None
    categoria_fiscal: Optional[CategoriaFiscalImpuestoEnum] = None
    notas_legales: Optional[str] = None
    cuenta_impuesto_vta: Optional[str] = None
    cuenta_impuesto_com: Optional[str] = None
    
    reparticiones: Optional[List[TipoImpuestoDistribucionCreate]] = None

class TipoImpuestoResponse(TipoImpuestoBase):
    id: int
    condiciones_asociadas: List[CondicionTributariaResponse] = []
    reparticiones: List[TipoImpuestoDistribucionResponse] = []

    class Config:
        from_attributes = True
