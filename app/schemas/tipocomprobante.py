from pydantic import BaseModel
from typing import Optional

class TipoComprobanteBase(BaseModel):
    codigo: Optional[str]
    descripcion: Optional[str]
    es_fiscal: Optional[bool]

class TipoComprobanteCreate(TipoComprobanteBase):
    pass

class TipoComprobanteResponse(TipoComprobanteBase):
    id: int

    class Config:
        from_attributes = True
