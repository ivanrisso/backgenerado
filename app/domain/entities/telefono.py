from typing import Optional
from dataclasses import dataclass

@dataclass
class Telefono:
    id: Optional[int] = None 
    tipo_tel_id: Optional[int] = None 
    prefijo: Optional[str] = None 
    numero: Optional[str] = None 
    domicilio_id: Optional[int] = None 
    