from dataclasses import dataclass
from typing import Optional, List, TYPE_CHECKING
from app.domain.menuitem import MenuItem

if TYPE_CHECKING:
    from app.domain.usuario import Usuario

@dataclass
class Rol:
    id: Optional[int]
    rol_nombre: Optional[str]
    es_admin: Optional[bool]
    usuarios: List["Usuario"]
    menuitems: List["MenuItem"]