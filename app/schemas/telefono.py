from pydantic import BaseModel
from typing import Optional

class TelefonoBase(BaseModel):
    tipo_tel_id: int
    prefijo: str
    numero: str
    domicilio_id: int

class TelefonoCreate(TelefonoBase):
    pass

class TelefonoUpdate(BaseModel):
    tipo_tel_id: Optional[int] = None
    prefijo: Optional[str] = None
    numero: Optional[str] = None
    domicilio_id: Optional[int] = None

class TelefonoResponse(TelefonoBase):
    id: int
    tipo_tel_id: int
    prefijo: str
    numero: str
    domicilio_id: int

    class Config:
        from_attributes = True