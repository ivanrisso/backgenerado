from dataclasses import dataclass
from typing import Optional, Any

@dataclass
class Cliente:
    id: Optional[int] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    razon_social: Optional[str] = None
    cuit: Optional[str] = None
    email: Optional[str] = None
    tipo_doc_id: Optional[int] = None
    condicion_iva_id: Optional[int] = None
    condicion_iibb_id: Optional[int] = None
    nro_iibb: Optional[str] = None
    condicion_iva: Optional[Any] = None
    condicion_iibb: Optional[Any] = None
