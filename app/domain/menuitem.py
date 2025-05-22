from dataclasses import dataclass
from typing import Optional, List, TYPE_CHECKING


if TYPE_CHECKING:
    from app.domain.rol import Rol

@dataclass
class MenuItem:
    id: Optional[int]
    nombre: Optional[str]
    path: Optional[str]
    parent_id: Optional[int]
    children: List["MenuItem"]
    parent: Optional["MenuItem"]
    roles: List["Rol"]