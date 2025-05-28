from typing import Optional
from dataclasses import dataclass

@dataclass
class RolMenuItem:
    rol_id: Optional[int] = None
    menu_item_id: Optional[int] = None
