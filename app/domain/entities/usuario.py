from dataclasses import dataclass, field
from typing import Optional, List
from app.domain.entities.rol import Rol

@dataclass
class Usuario:
    id: Optional[int]
    usuario_email: Optional[str]
    usuario_password: Optional[str]
    nombre: Optional[str]
    apellido: Optional[str]
    plain_password: Optional[str] = None
    roles: List[Rol] = field(default_factory=list)    
