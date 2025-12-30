from pydantic import BaseModel
from typing import Optional

class CondicionIvaCreate(BaseModel):
    codigo: int
    descripcion: str

class CondicionIvaUpdate(BaseModel):
    codigo: Optional[int] = None
    descripcion: Optional[str] = None

class CondicionIvaResponse(BaseModel):
    id: int 
    codigo: int
    descripcion: str

    class Config:
        from_attributes = True
