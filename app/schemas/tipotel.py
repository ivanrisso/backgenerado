# ✅ app/schemas/tipotel.py
from pydantic import BaseModel
from typing import Optional

class TipoTelCreate(BaseModel):
    nombre: str

class TipoTelUpdate(BaseModel):
    nombre: Optional[str] = None

class TipoTelResponse(BaseModel):
    id: int 
    nombre: str

    class Config:
        from_attributes = True
        