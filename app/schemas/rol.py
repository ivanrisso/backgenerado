from pydantic import BaseModel
from typing import Optional

class RolBase(BaseModel):
    rol_nombre: str
    es_admin: bool

class RolCreate(RolBase):
    pass

class RolResponse(RolBase):
    id: int

    class Config:
        from_attributes = True