# ✅ app/schemas/cliente.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class ClienteCreate(BaseModel):
    nombre: str
    apellido: str
    razon_social: Optional[str] = None
    cuit: Optional[str] = None
    email: EmailStr
    tipo_doc_id: int
    iva_id: int

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    razon_social: Optional[str] = None
    cuit: Optional[str] = None
    email: Optional[EmailStr] = None
    tipo_doc_id: Optional[int] = None
    iva_id: Optional[int] = None

class ClienteResponse(BaseModel):
    id: int
    nombre: str
    apellido: str
    razon_social: Optional[str]
    cuit: Optional[str]
    email: EmailStr
    tipo_doc_id: int
    iva_id: int

    class Config:
        from_attributes = True
