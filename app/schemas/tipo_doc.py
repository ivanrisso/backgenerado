from pydantic import BaseModel

class TipoDocBase(BaseModel):
    tipo_doc_nombre: str
    habilitado: bool

class TipoDocCreate(TipoDocBase):
    pass

class TipoDocResponse(TipoDocBase):
    id: int

    class Config:
        from_attributes = True
