from dataclasses import dataclass
from typing import Optional

@dataclass
class Voucher:
    id: str  # Mapped from CupIte (Primary Key)
    nro_voucher: str # Mapped from CupNroVou / CupVou1
    monto_neto_ope: float # CupNetoOpe (Subtotal)
    monto_neto_gsa: float # CupNetoGSA (Values to subtract to get taxable base)
    monto_impuestos: float # CupImpoTax (Other Taxes)
    descripcion: str
    ref_cliente: str # Mapped from CupCliente
    sistema_origen: str # "TANGO" or "SQL_SERVER"
    usado: bool = False
