from pydantic import BaseModel
from typing import Optional

class RolMenuItemBase(BaseModel):
    rol_id: Optional[int]
    menu_item_id: Optional[int]

class RolMenuItemCreate(BaseModel):
    rol_id: int
    menu_item_id: int

class RolMenuItemUpdate(BaseModel):
    rol_id: int
    menu_item_id: int

class RolMenuItemResponse(RolMenuItemBase):
    rol_id: int
    menu_item_id: int
    
        
    class Config:
        from_attributes = True
