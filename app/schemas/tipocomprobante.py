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

class TipoComprobanteUpdate(BaseModel):
    codigo: Optional[str] = None
    descripcion: Optional[str] = None
    es_fiscal: Optional[bool] = None

class TipoComprobanteResponse(TipoComprobanteBase):
    id: int
    codigo: str
    descripcion: str
    es_fiscal: bool

    class Config:
        from_attributes = True
