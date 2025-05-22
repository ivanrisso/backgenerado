from pydantic import BaseModel

class ConceptoBase(BaseModel):
    codigo: str
    descripcion: str

class ConceptoCreate(ConceptoBase):
    pass

class ConceptoResponse(ConceptoBase):
    id: int

    class Config:
        from_attributes = True
