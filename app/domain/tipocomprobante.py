from typing import Optional
from pydantic import BaseModel


class TipoComprobante(BaseModel):
    id: Optional[int]
    codigo: Optional[str]
    descripcion: Optional[str]
    es_fiscal: Optional[bool]
    
    class Config:
        from_attributes = True
    