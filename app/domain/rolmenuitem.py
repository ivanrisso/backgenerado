from dataclasses import dataclass
from typing import Optional, List
from decimal import Decimal
from datetime import date, datetime

@dataclass
class RolMenuItem:
    rol_id: Optional[int]
    menu_item_id: Optional[int]