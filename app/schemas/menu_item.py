from pydantic import BaseModel
from typing import Optional
from app.schemas.usuario import RolResponse

class MenuItemCreate(BaseModel):
    nombre: str
    path: Optional[str] = None
    parent_id: Optional[int] = None
    orden: Optional[int] = 0
    role_ids: Optional[list[int]] = None

class MenuItemUpdate(BaseModel):
    nombre: Optional[str] = None
    path: Optional[str] = None
    parent_id: Optional[int] = None
    role_ids: Optional[list[int]] = None

class MenuItemResponse(BaseModel):
    id: int
    nombre: str
    path: Optional[str] = None
    parent_id: Optional[int] = None
    roles: list["RolResponse"] = []

    class Config:
        from_attributes = True
