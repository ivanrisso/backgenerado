from pydantic import BaseModel
from typing import Optional


class MonedaCreate(BaseModel):
    codigo: str
    descripcion: str
    codigo_arca: str

class MonedaUpdate(BaseModel):
    codigo: Optional[str] = None
    descripcion: Optional[str] = None
    codigo_arca: Optional[str] = None

class MonedaResponse(BaseModel):
    id: int
    codigo: str
    descripcion: str
    codigo_arca: str

    class Config:
        from_attributes = True
