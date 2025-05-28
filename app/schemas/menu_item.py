from pydantic import BaseModel
from typing import Optional

class MenuItemCreate(BaseModel):
    nombre: str
    path: str
    parent_id: int

class MenuItemUpdate(BaseModel):
    nombre: Optional[str] = None
    path: Optional[str] = None
    parent_id: Optional[int] = None

class MenuItemResponse(BaseModel):
    id: int
    nombre: str
    path: str
    parent_id: int

    class Config:
        from_attributes = True