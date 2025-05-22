from pydantic import BaseModel
from typing import Optional

class TipoDomBase(BaseModel):
    nombre: Optional[str]

class TipoDomCreate(TipoDomBase):
    pass

class TipoDomResponse(TipoDomBase):
    id: int

    class Config:
        from_attributes = True
