# ✅ app/schemas/usuario.py
from pydantic import BaseModel, EmailStr

class UsuarioCreate(BaseModel):
    usuario_email: EmailStr
    usuario_password: str

class UsuarioUpdate(BaseModel):
    pass

class UsuarioResponse(BaseModel):
    usuario_email: str


    class Config:
        from_attributes = True
        