from pydantic import BaseModel
from typing import Optional

class RolMenuItemBase(BaseModel):
    rol_id: Optional[int]
    menu_item_id: Optional[int]

class RolMenuItemCreate(RolMenuItemBase):
    pass

class RolMenuItemResponse(RolMenuItemBase):
    class Config:
        from_attributes = True
