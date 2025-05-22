from typing import Optional
from pydantic import BaseModel


class Operador(BaseModel):
    id: Optional[int]
    cliente_id: Optional[int]

    class Config:
        from_attributes = True
