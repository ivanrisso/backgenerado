from dataclasses import dataclass
from typing import Optional

@dataclass
class Usuario:
    id: Optional[int]
    usuario_email: Optional[str]
    usuario_password: Optional[str]
    nombre: Optional[str]
    apellido: Optional[str]
    plain_password: Optional[str] = None
    
