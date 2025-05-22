from pydantic import BaseModel
from typing import Optional


class LocalidadBase(BaseModel):
    localidad_nombre: Optional[str]
    cod_postal: Optional[str]
    provincia_id: Optional[int]


class LocalidadCreate(LocalidadBase):
    pass


class LocalidadResponse(LocalidadBase):
    id: int

    class Config:
        from_attributes = True
