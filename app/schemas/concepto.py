from pydantic import BaseModel
from typing import Optional

class ConceptoCreate(BaseModel):
    codigo: str
    descripcion: str

class ConceptoUpdate(BaseModel):
    codigo: Optional[str] = None
    descripcion: Optional[str] = None

class ConceptoResponse(BaseModel):
    id: int
    codigo: Optional[str] = None
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True
