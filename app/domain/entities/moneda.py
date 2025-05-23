from typing import Optional, List
from pydantic import BaseModel

class Moneda(BaseModel):
    id: Optional[int]
    codigo: Optional[str]
    descripcion: Optional[str]

    class Config:
        from_attributes = True
