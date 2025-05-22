from typing import Optional
from pydantic import BaseModel

class Usuario(BaseModel):
    id: Optional[int]
    usuario_email: Optional[str]
    usuario_password: Optional[str]
    nombre: Optional[str]
    apellido: Optional[str]
    plain_password: Optional[str] 
    
    class Config:
        from_attributes = True
    