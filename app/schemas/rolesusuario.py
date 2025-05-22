from pydantic import BaseModel
from typing import Optional

class RolesUsuarioBase(BaseModel):
    usuario_id: Optional[int]
    rol_id: Optional[int]

class RolesUsuarioCreate(RolesUsuarioBase):
    pass

class RolesUsuarioResponse(RolesUsuarioBase):
    class Config:
        from_attributes = True
