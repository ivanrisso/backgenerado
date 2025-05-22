from pydantic import BaseModel

class TelefonoBase(BaseModel):
    tipo_tel_id: int
    prefijo: str
    numero: str
    domicilio_id: int

class TelefonoCreate(TelefonoBase):
    pass

class TelefonoResponse(TelefonoBase):
    id: int

    class Config:
        from_attributes = True