from typing import Optional
from dataclasses import dataclass

@dataclass    
class TipoComprobante:
    id: Optional[int] = None
    codigo: Optional[str] = None
    descripcion: Optional[str] = None
    es_fiscal: Optional[bool] = None
    codigo_arca: Optional[str] = None
