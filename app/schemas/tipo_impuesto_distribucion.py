from pydantic import BaseModel
from typing import Optional, List
from app.domain.entities.enums import TipoDistribucionImpuestoEnum, TipoReparticionBaseImpuestoEnum

class TipoImpuestoEtiquetaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class TipoImpuestoEtiquetaCreate(TipoImpuestoEtiquetaBase):
    pass

class TipoImpuestoEtiquetaUpdate(TipoImpuestoEtiquetaBase):
    nombre: Optional[str] = None

class TipoImpuestoEtiquetaResponse(TipoImpuestoEtiquetaBase):
    id: int
    class Config:
        from_attributes = True

class TipoImpuestoDistribucionBase(BaseModel):
    tipo_reparticion: TipoDistribucionImpuestoEnum = TipoDistribucionImpuestoEnum.FACTURA
    factor_porcentaje: float = 100.0
    basado_en: TipoReparticionBaseImpuestoEnum = TipoReparticionBaseImpuestoEnum.IMPUESTO
    etiqueta_id: Optional[int] = None
    cuenta_contable: Optional[str] = None

class TipoImpuestoDistribucionCreate(TipoImpuestoDistribucionBase):
    pass

class TipoImpuestoDistribucionUpdate(TipoImpuestoDistribucionBase):
    pass

class TipoImpuestoDistribucionResponse(TipoImpuestoDistribucionBase):
    id: int
    tipo_impuesto_id: int
    etiqueta: Optional[TipoImpuestoEtiquetaResponse] = None
    class Config:
        from_attributes = True
