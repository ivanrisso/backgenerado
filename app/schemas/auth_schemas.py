from pydantic import BaseModel, EmailStr
from typing import Optional

# Esquema para el registro de usuario
class UsuarioCreate(BaseModel):
    usuario_email: EmailStr
    usuario_password: str
    nombre: str
    apellido: str

# Esquema para la autenticación (formulario de login)
class UsuarioLogin(BaseModel):
    username: EmailStr
    password: str

# Esquema de respuesta con el token
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Esquema para decodificar payloads de JWT
class TokenData(BaseModel):
    sub: Optional[str] = None