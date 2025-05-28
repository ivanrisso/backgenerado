from pydantic import BaseModel
from typing import Optional

class PaisCreate(BaseModel):
    codigo: str
    nombre: str

class PaisUpdate(BaseModel):
    codigo: Optional[str] = None
    nombre: Optional[str] = None

class PaisResponse(BaseModel):
    id: int
    codigo: str
    nombre: str

    class Config:
        from_attributes = True
