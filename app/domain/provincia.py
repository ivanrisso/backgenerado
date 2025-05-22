from typing import Optional
from pydantic import BaseModel

class Provincia(BaseModel):
    id: Optional[int]
    provincia_nombre: Optional[str]
    pais_id: Optional[int]

    class Config:
        from_attributes = True
