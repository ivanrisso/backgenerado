from dataclasses import dataclass
from typing import Optional

@dataclass    
class TipoDoc:
    id: Optional[int] = None
    tipo_doc_nombre: Optional[str] = None
    habilitado: Optional[bool] = None
        