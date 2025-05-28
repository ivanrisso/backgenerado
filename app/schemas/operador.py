from pydantic import BaseModel
from typing import Optional


class OperadorCreate(BaseModel):
    cliente_id: Optional[int]

class OperadorUpdate(BaseModel):
    cliente_id: Optional[int]

class OperadorResponse(BaseModel):
    id: int

    class Config:
        from_attributes = True
