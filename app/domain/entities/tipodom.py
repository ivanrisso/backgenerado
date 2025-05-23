from dataclasses import dataclass
from typing import Optional, List
from pydantic import BaseModel

class TipoDom(BaseModel):
    id: Optional[int]
    nombre: Optional[str]
    
    class Config:
        from_attributes = True
    