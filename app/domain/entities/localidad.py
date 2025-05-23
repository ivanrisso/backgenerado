from typing import Optional
from pydantic import BaseModel


class Localidad(BaseModel):
    id: Optional[int]
    localidad_nombre: Optional[str]
    cod_postal: Optional[str]
    provincia_id: Optional[int]
    
    class Config:
        from_attributes = True
    