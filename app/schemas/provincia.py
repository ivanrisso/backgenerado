from pydantic import BaseModel
from typing import Optional


class ProvinciaCreate(BaseModel):
    provincia_nombre: Optional[str]
    pais_id: Optional[int]

class ProvinciaUpdate(BaseModel):
    provincia_nombre: Optional[str]
    pais_id: Optional[int]

class ProvinciaResponse(BaseModel):
    id: int
    provincia_nombre: Optional[str]
    pais_id: Optional[int]
    
    class Config:
        from_attributes = True
