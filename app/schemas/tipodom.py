from pydantic import BaseModel
from typing import Optional

class TipoDomBase(BaseModel):
    nombre: Optional[str]

class TipoDomCreate(TipoDomBase):
    pass

class TipoDomUpdate(BaseModel):
    nombre: Optional[str] = None

class TipoDomResponse(TipoDomBase):
    id: int
    nombre: str

    class Config:
        from_attributes = True
