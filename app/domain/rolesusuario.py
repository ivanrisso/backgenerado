from typing import Optional
from pydantic import BaseModel


class RolesUsuario(BaseModel):
    usuario_id: Optional[int]
    rol_id: Optional[int]
    
    class Config:
        from_attributes = True
    