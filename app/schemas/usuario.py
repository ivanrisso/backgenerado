from pydantic import BaseModel, EmailStr
from typing import Optional

class UsuarioBase(BaseModel):
    usuario_email: EmailStr
    nombre: str
    apellido: str

class UsuarioCreate(UsuarioBase):
    usuario_password: str

class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True