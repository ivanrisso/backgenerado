from typing import Optional, List
from pydantic import BaseModel


class Cliente(BaseModel):
    id: Optional[int]
    nombre: Optional[str]
    apellido: Optional[str]
    razon_social: Optional[str]
    cuit: Optional[str]
    email: Optional[str]
    tipo_doc_id: Optional[int]
    iva_id: Optional[int]
    
    class Config:
        from_attributes = True
