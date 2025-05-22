from pydantic import BaseModel
from typing import Optional

class ProvinciaBase(BaseModel):
    provincia_nombre: Optional[str]
    pais_id: Optional[int]

class ProvinciaCreate(ProvinciaBase):
    pass

class ProvinciaResponse(ProvinciaBase):
    id: int

    class Config:
        from_attributes = True
