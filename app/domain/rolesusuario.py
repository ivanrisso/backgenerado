from dataclasses import dataclass
from typing import Optional, List

@dataclass
class RolesUsuario:
    usuario_id: Optional[int]
    rol_id: Optional[int]