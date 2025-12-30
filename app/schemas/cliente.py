from pydantic import BaseModel, EmailStr
from typing import Optional
from app.schemas.condicion_tributaria import CondicionTributariaResponse

class ClienteCreate(BaseModel):
    nombre: str
    apellido: str
    razon_social: Optional[str] = None
    cuit: Optional[str] = None
    email: EmailStr
    tipo_doc_id: int
    condicion_iva_id: Optional[int] = None
    condicion_iibb_id: Optional[int] = None
    nro_iibb: Optional[str] = None

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    razon_social: Optional[str] = None
    cuit: Optional[str] = None
    email: Optional[EmailStr] = None
    tipo_doc_id: Optional[int] = None
    condicion_iva_id: Optional[int] = None
    condicion_iibb_id: Optional[int] = None
    nro_iibb: Optional[str] = None

class ClienteResponse(BaseModel):
    id: int
    nombre: str
    apellido: str
    razon_social: Optional[str]
    cuit: Optional[str]
    email: EmailStr
    tipo_doc_id: int
    condicion_iva_id: Optional[int] = None
    condicion_iibb_id: Optional[int] = None
    nro_iibb: Optional[str] = None
    
    condicion_iva: Optional[CondicionTributariaResponse] = None
    condicion_iibb: Optional[CondicionTributariaResponse] = None

    class Config:
        from_attributes = True
