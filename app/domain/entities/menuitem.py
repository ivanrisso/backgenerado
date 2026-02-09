from typing import Optional, List, TYPE_CHECKING
from dataclasses import dataclass, field

if TYPE_CHECKING:
    from app.domain.entities.rol import Rol

@dataclass
class MenuItem:
    id: Optional[int] = None
    nombre: Optional[str] = None
    path: Optional[str] = None
    parent_id: Optional[int] = None
    orden: int = 0
    roles: List['Rol'] = field(default_factory=list) # Forward ref if needed, or import

    