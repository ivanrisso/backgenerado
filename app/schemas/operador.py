from pydantic import BaseModel
from typing import Optional

class OperadorBase(BaseModel):
    cliente_id: Optional[int]

class OperadorCreate(OperadorBase):
    pass

class OperadorResponse(OperadorBase):
    id: int

    class Config:
        from_attributes = True
