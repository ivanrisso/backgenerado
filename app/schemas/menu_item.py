from pydantic import BaseModel
from typing import Optional

class MenuItemBase(BaseModel):
    nombre: str
    path: Optional[str]
    parent_id: Optional[int]

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemResponse(MenuItemBase):
    id: int

    class Config:
        from_attributes = True