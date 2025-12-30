from typing import Optional, List
from dataclasses import dataclass, field
from app.domain.entities.enums import (
    TipoAplicacionEnum, BaseTributarioEnum, AmbitoImpuestoEnum, 
    CategoriaImpuestoEnum, TipoUsoImpuestoEnum, MetodoCalculoImpuestoEnum,
    AmbitoUsoImpuestoEnum, CategoriaFiscalImpuestoEnum
)
from app.domain.entities.condiciontributaria import CondicionTributaria
from app.domain.entities.tipo_impuesto_distribucion import TipoImpuestoDistribucion

@dataclass
class TipoImpuesto:
    id: Optional[int] = None
    codigo_afip: str = ""
    nombre: str = ""
    descripcion: str = ""
    tipo_aplicacion: TipoAplicacionEnum = TipoAplicacionEnum.SUMA
    base_calculo: BaseTributarioEnum = BaseTributarioEnum.SUBTOTAL
    ambito: AmbitoImpuestoEnum = AmbitoImpuestoEnum.NACIONAL
    categoria: CategoriaImpuestoEnum = CategoriaImpuestoEnum.IMPUESTO_DIRECTO
    porcentaje: Optional[float] = None
    editable: bool = True
    obligatorio: bool = False
    activo: bool = True
    
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
    
    condiciones_asociadas: List[CondicionTributaria] = field(default_factory=list)
    reparticiones: List[TipoImpuestoDistribucion] = field(default_factory=list)