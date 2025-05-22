from typing import Optional
from pydantic import BaseModel

class Telefono(BaseModel):
    id: Optional[int]
    tipo_tel_id: Optional[int]
    prefijo: Optional[str]
    numero: Optional[str]
    domicilio_id: Optional[int]
    
    class Config:
        from_attributes = True
    