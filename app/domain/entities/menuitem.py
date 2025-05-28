from typing import Optional
from dataclasses import dataclass

@dataclass
class MenuItem:
    id: Optional[int] = None
    nombre: Optional[str] = None
    path: Optional[str] = None
    parent_id: Optional[int] = None
    