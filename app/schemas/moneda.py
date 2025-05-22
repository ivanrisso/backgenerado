from pydantic import BaseModel

class MonedaBase(BaseModel):
    codigo: str
    descripcion: str

class MonedaCreate(MonedaBase):
    pass

class MonedaResponse(MonedaBase):
    id: int

    class Config:
        from_attributes = True
