from typing import Optional
from pydantic import BaseModel


class Concepto(BaseModel):
    id: Optional[int]
    codigo: Optional[str]
    descripcion: Optional[str]
    
    class Config:
        from_attributes = True
