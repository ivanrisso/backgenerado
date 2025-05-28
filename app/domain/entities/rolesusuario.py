from typing import Optional
from dataclasses import dataclass

@dataclass
class RolesUsuario:
    usuario_id: Optional[int] = None
    rol_id: Optional[int] = None
