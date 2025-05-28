from pydantic import BaseModel
from typing import Optional


class RolCreate(BaseModel):
    rol_nombre: str
    es_admin: bool

class RolUpdate(BaseModel):
    rol_nombre: Optional[str] = None
    es_admin: Optional[bool] = None

class RolResponse(BaseModel):
    id: int
    rol_nombre: str
    es_admin: bool

    class Config:
        from_attributes = True