# app/domain/enums.py
from enum import Enum

class TipoAplicacionEnum(str, Enum):
    SUMA = "SUMA"
    DESCUENTO = "DESCUENTO"
    NEUTRO = "NEUTRO"

class BaseTributarioEnum(str, Enum):
    SUBTOTAL = "SUBTOTAL"
    TOTAL = "TOTAL"
    NETO_GRAVADO = "NETO_GRAVADO"
    OTROS = "OTROS"

class AmbitoImpuestoEnum(str, Enum):
    NACIONAL = "NACIONAL"
    PROVINCIAL = "PROVINCIAL"
    MUNICIPAL = "MUNICIPAL"

class CategoriaImpuestoEnum(str, Enum):
    IMPUESTO_DIRECTO = "IMPUESTO_DIRECTO"
    PERCEPCION = "PERCEPCION"
    RETENCION = "RETENCION"
    TASA = "TASA"
    OTRO = "OTRO"

class TipoUsoImpuestoEnum(str, Enum):
    VENTAS = "VENTAS"
    COMPRAS = "COMPRAS"
    OTRO = "OTRO"
    RETENCION_PAGO_PROVEEDOR = "RETENCION_PAGO_PROVEEDOR"
    RETENCION_PAGO_CLIENTE = "RETENCION_PAGO_CLIENTE"

class MetodoCalculoImpuestoEnum(str, Enum):
    PORCENTAJE = "PORCENTAJE"
    FIJO = "FIJO"
    PORCENTAJE_SOBRE_PRECIO = "PORCENTAJE_SOBRE_PRECIO"
    GRUPO = "GRUPO"

class AmbitoUsoImpuestoEnum(str, Enum):
    BIENES = "BIENES"
    SERVICIOS = "SERVICIOS"
    AMBOS = "AMBOS"

class CategoriaFiscalImpuestoEnum(str, Enum):
    AE = "AE"
    E = "E"
    S = "S"
    Z = "Z"
    G = "G"
    O = "O"
    K = "K"
    L = "L"
    M = "M"
    B = "B"

class TipoArticuloEnum(str, Enum):
    PRODUCTO = "PRODUCTO"
    SERVICIO = "SERVICIO"
    CONSUMIBLE = "CONSUMIBLE"

class TipoDistribucionImpuestoEnum(str, Enum):
    FACTURA = "FACTURA"
    REEMBOLSO = "REEMBOLSO"

class TipoReparticionBaseImpuestoEnum(str, Enum):
    BASE = "BASE"
    IMPUESTO = "IMPUESTO"
