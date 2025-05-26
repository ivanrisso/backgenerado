#app/domain/entities/cliente.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class Cliente:
    id: Optional[int]
    nombre: Optional[str]
    apellido: Optional[str]
    razon_social: Optional[str]
    cuit: Optional[str]
    email: str
    tipo_doc_id: Optional[int]
    iva_id: Optional[int]
