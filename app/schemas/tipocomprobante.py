from pydantic import BaseModel
from typing import Optional

class TipoComprobanteBase(BaseModel):
    codigo: Optional[str]
    descripcion: Optional[str]
    es_fiscal: Optional[bool]

class TipoComprobanteCreate(BaseModel):
    codigo: str
    descripcion: str
    es_fiscal: bool
    codigo_arca: str

class TipoComprobanteUpdate(BaseModel):
    codigo: Optional[str] = None
    descripcion: Optional[str] = None
    es_fiscal: Optional[bool] = None
    codigo_arca: Optional[str] = None

class TipoComprobanteResponse(TipoComprobanteBase):
    id: int
    codigo: str
    descripcion: str
    es_fiscal: bool
    codigo_arca: str

    class Config:
        from_attributes = True
