from pydantic import BaseModel
from typing import Optional


class MonedaCreate(BaseModel):
    codigo: str
    descripcion: str

class MonedaUpdate(BaseModel):
    codigo: Optional[str] = None
    descripcion: Optional[str] = None

class MonedaResponse(BaseModel):
    id: int
    codigo: str
    descripcion: str

    class Config:
        from_attributes = True
