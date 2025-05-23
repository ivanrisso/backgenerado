from typing import Optional
from pydantic import BaseModel


class MenuItem(BaseModel):
    id: Optional[int]
    nombre: Optional[str]
    path: Optional[str]
    parent_id: Optional[int]
    
    class Config:
        from_attributes = True
    