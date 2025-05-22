from typing import Optional
from pydantic import BaseModel

class Rol(BaseModel):
    id: Optional[int]
    rol_nombre: Optional[str]
    es_admin: Optional[bool]

    class Config:
        from_attributes = True
