from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, TYPE_CHECKING
from app.domain.tipodoc import TipoDoc


if TYPE_CHECKING:
    from app.domain.iva import Iva
    from app.domain.comprobante import Comprobante
    from app.domain.domicilio import Domicilio
    from app.domain.clienteimpuesto import ClienteImpuesto
    from app.domain.cuentacorriente import CuentaCorriente
    from app.domain.operador import Operador

@dataclass
class Cliente:
    id: Optional[int]
    nombre: Optional[str]
    apellido: Optional[str]
    razon_social: Optional[str]
    cuit: Optional[str]
    email: Optional[str]
    tipo_doc_id: Optional[int]
    iva_id: Optional[int]
    iva: Optional["Iva"]
    tipo_doc: Optional[TipoDoc]
    comprobantes: List["Comprobante"]
    domicilios: List["Domicilio"]
    impuestos: List["ClienteImpuesto"]
    movimientos_cc: List["CuentaCorriente"]
    operadores: List["Operador"]