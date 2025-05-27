# ✅ app/schemas/usuario.py
from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UsuarioCreate(BaseModel):
    usuario_email: EmailStr
    usuario_password: str

class UsuarioUpdate(BaseModel):
    pass

class UsuarioResponse(BaseModel):
    usuario_email: str

class RolResponse(BaseModel):
    rol_nombre: str

class UsuarioResponseConRoles(BaseModel):
    usuario_email: str
    nombre: str
    apellido: str
    roles: Optional[List[RolResponse]] = None

    class Config:
        from_attributes = True
        
        