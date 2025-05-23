from typing import Optional, List
from pydantic import BaseModel

class Pais(BaseModel):
    id: Optional[int]
    codigo: Optional[str]
    nombre: Optional[str]

    class Config:
        from_attributes = True
