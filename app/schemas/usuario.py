# ✅ app/schemas/usuario.py
from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UsuarioCreate(BaseModel):
    usuario_email: EmailStr
    usuario_password: str
    nombre: str
    apellido: str
    role_ids: List[int] = []

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    usuario_email: Optional[EmailStr] = None
    usuario_password: Optional[str] = None
    role_ids: Optional[List[int]] = None

class RolResponse(BaseModel):
    id: int
    rol_nombre: str
    es_admin: bool

    class Config:
        from_attributes = True

class UsuarioResponse(BaseModel):
    id: int
    usuario_email: str
    nombre: str
    apellido: str
    roles: List[RolResponse] = []

    class Config:
        from_attributes = True
        
        