from pydantic import BaseModel
from typing import Optional

class TipoDocBase(BaseModel):
    tipo_doc_nombre: str
    habilitado: bool

class TipoDocCreate(TipoDocBase):
    pass

class TipoDocUpdate(BaseModel):
    tipo_doc_nombre: Optional[str] = None 
    habilitado: Optional[bool] = None

class TipoDocResponse(TipoDocBase):
    id: int

    class Config:
        from_attributes = True
