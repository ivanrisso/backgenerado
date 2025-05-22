from typing import Optional
from pydantic import BaseModel

class Domicilio(BaseModel):
    id: Optional[int]
    calle: Optional[str]
    numero: Optional[int]
    cliente_id: Optional[int]
    tipo_dom_id: Optional[int]
    localidad_id: Optional[int]

    class Config:
        from_attributes = True
