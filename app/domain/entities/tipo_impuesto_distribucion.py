from dataclasses import dataclass, field
from typing import Optional
from app.domain.entities.enums import TipoDistribucionImpuestoEnum, TipoReparticionBaseImpuestoEnum

@dataclass
class TipoImpuestoEtiqueta:
    id: Optional[int] = None
    nombre: str = ""
    descripcion: Optional[str] = None

@dataclass
class TipoImpuestoDistribucion:
    id: Optional[int] = None
    tipo_impuesto_id: Optional[int] = None
    tipo_reparticion: TipoDistribucionImpuestoEnum = TipoDistribucionImpuestoEnum.FACTURA
    factor_porcentaje: float = 100.0
    basado_en: TipoReparticionBaseImpuestoEnum = TipoReparticionBaseImpuestoEnum.IMPUESTO
    etiqueta_id: Optional[int] = None
    cuenta_contable: Optional[str] = None
    
    # Relaciones opcionales (cargadas por el repo)
    etiqueta: Optional[TipoImpuestoEtiqueta] = None
