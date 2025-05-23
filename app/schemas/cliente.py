from pydantic import BaseModel, EmailStr
from typing import Optional

class ClienteBase(BaseModel):
    nombre: str
    apellido: str
    razon_social: Optional[str]
    cuit: Optional[str]
    email: Optional[EmailStr]
    tipo_doc_id: int
    iva_id: int

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(ClienteBase):
    nombre: str
    apellido: str
    razon_social: Optional[str]
    cuit: Optional[str]
    email: Optional[EmailStr]
    tipo_doc_id: int
    iva_id: int

class ClienteResponse(ClienteBase):
    id: int

    class Config:
        from_attributes = True