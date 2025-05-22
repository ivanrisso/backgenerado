from pydantic import BaseModel
from typing import Optional

class TipoTelBase(BaseModel):
    nombre: Optional[str]

class TipoTelCreate(TipoTelBase):
    pass

class TipoTelResponse(TipoTelBase):
    id: int

    class Config:
        from_attributes = True
