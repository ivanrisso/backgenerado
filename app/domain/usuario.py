from dataclasses import dataclass
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.rol import Rol
    from app.domain.auditoriacomprobante import AuditoriaComprobante


@dataclass
class Usuario:
    id: Optional[int]
    usuario_email: Optional[str]
    usuario_password: Optional[str]
    nombre: Optional[str]
    apellido: Optional[str]
    roles: List["Rol"]
    auditorias: List["AuditoriaComprobante"]
    plain_password: Optional[str] = None    
    