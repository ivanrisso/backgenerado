from typing import Optional, List
from pydantic import BaseModel, EmailStr


class Cliente(BaseModel):
    id: Optional[int] = None
    nombre: Optional[str]
    apellido: Optional[str]
    razon_social: Optional[str]
    cuit: Optional[str]
    email: EmailStr
    tipo_doc_id: Optional[int]
    iva_id: Optional[int]
    
    class Config:
        from_attributes = True
