from pydantic import BaseModel
from typing import Optional

class LocalidadCreate(BaseModel):
    localidad_nombre: str
    cod_postal: str
    provincia_id: int

class LocalidadUpdate(BaseModel):
    localidad_nombre: Optional[str] = None
    cod_postal: Optional[str] = None
    provincia_id: Optional[int] = None

class LocalidadResponse(BaseModel):
    id: int
    localidad_nombre: str
    cod_postal: str
    provincia_id: int

    class Config:
        from_attributes = True
