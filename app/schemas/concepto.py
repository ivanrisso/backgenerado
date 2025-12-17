from pydantic import BaseModel
from typing import Optional

class ConceptoCreate(BaseModel):
    codigo: str
    descripcion: str
    codigo_arca: str

class ConceptoUpdate(BaseModel):
    codigo: Optional[str] = None
    descripcion: Optional[str] = None
    codigo_arca: Optional[str] = None

class ConceptoResponse(BaseModel):
    id: int
    codigo: Optional[str] = None
    descripcion: Optional[str] = None
    codigo_arca: str

    class Config:
        from_attributes = True
