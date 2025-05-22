from pydantic import BaseModel
from typing import Optional

class DomicilioBase(BaseModel):
    calle: str
    numero: int
    cliente_id: int
    tipo_dom_id: int
    localidad_id: int

class DomicilioCreate(DomicilioBase):
    pass

class DomicilioResponse(DomicilioBase):
    id: int

    class Config:
        from_attributes = True