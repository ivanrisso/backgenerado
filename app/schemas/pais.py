from pydantic import BaseModel
from typing import Optional

class PaisBase(BaseModel):
    codigo: Optional[str]
    nombre: Optional[str]

class PaisCreate(PaisBase):
    pass

class PaisResponse(PaisBase):
    id: int

    class Config:
        from_attributes = True
