from typing import Optional
from pydantic import BaseModel

class TipoTel(BaseModel):
    id: Optional[int]
    nombre: Optional[str]
    
    class Config:
        from_attributes = True
    