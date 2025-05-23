# app/domain/enums.py
from enum import Enum

class TipoAplicacionEnum(str, Enum):
    SUMA = "suma"
    DESCUENTO = "descuento"
    NEUTRO = "neutro"

class BaseTributarioEnum(str, Enum):
    SUBTOTAL = "subtotal"
    TOTAL = "total"
    NETO_GRAVADO = "neto_gravado"
    OTROS = "otros"
