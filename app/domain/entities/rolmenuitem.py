from typing import Optional
from pydantic import BaseModel

class RolMenuItem(BaseModel):
    rol_id: Optional[int]
    menu_item_id: Optional[int]
    
    class Config:
        from_attributes = True
    