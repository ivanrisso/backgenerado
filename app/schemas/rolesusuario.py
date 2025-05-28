from pydantic import BaseModel
from typing import Optional


class RolesUsuarioCreate(BaseModel):
    usuario_id: int
    rol_id: int

class RolesUsuarioUpdate(BaseModel):
    usuario_id: int
    rol_id: int

class RolesUsuarioResponse(BaseModel):
    usuario_id: int
    rol_id: int
    
    class Config:
        from_attributes = True
