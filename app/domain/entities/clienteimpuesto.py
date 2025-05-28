from typing import Optional
from dataclasses import dataclass

@dataclass
class ClienteImpuesto:
    id: Optional[int] = None
    cliente_id: Optional[int] = None
    tipo_impuesto_id: Optional[int] = None
    aplica: Optional[bool] = None
    alicuota: Optional[float] = None
    observaciones: Optional[str] = None
