#app/domain/entities/cliente.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class Cliente:
    id: Optional[int] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    razon_social: Optional[str] = None
    cuit: Optional[str] = None
    email: Optional[str] = None
    tipo_doc_id: Optional[int] = None
    iva_id: Optional[int] = None
