from pydantic import BaseModel
from typing import Optional

class DomicilioCreate(BaseModel):
    calle: str
    numero: int
    cliente_id: int
    tipo_dom_id: int
    localidad_id: int

class DomicilioUpdate(BaseModel):
    calle: Optional[str] = None
    numero: Optional[int] = None
    cliente_id: Optional[int] = None
    tipo_dom_id: Optional[int] = None
    localidad_id: Optional[int] = None

class DomicilioResponse(BaseModel):
    id: int
    calle: str
    numero: int
    cliente_id: int
    tipo_dom_id: int
    localidad_id: int

    class Config:
        from_attributes = True