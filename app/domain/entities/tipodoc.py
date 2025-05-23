from typing import Optional
from pydantic import BaseModel
    
class TipoDoc(BaseModel):
    id: Optional[int]
    tipo_doc_nombre: Optional[str]
    habilitado: Optional[bool]
    
    class Config:
        from_attributes = True
    