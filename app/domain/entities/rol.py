from typing import Optional
from dataclasses import dataclass

@dataclass
class Rol:
    id: Optional[int] = None
    rol_nombre: Optional[str] = None
    es_admin: Optional[bool] = None
