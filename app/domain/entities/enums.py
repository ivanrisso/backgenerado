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

class AmbitoImpuestoEnum(str, Enum):
    NACIONAL = "nacional"
    PROVINCIAL = "provincial"
    MUNICIPAL = "municipal"

class CategoriaImpuestoEnum(str, Enum):
    IMPUESTO_DIRECTO = "impuesto_directo"
    PERCEPCION = "percepcion"
    RETENCION = "retencion"
    TASA = "tasa"
    OTRO = "otro"

class TipoUsoImpuestoEnum(str, Enum):
    VENTAS = "ventas"
    COMPRAS = "compras"
    OTRO = "otro"
    RETENCION_PAGO_PROVEEDOR = "retencion_pago_proveedor"
    RETENCION_PAGO_CLIENTE = "retencion_pago_cliente"

class MetodoCalculoImpuestoEnum(str, Enum):
    PORCENTAJE = "porcentaje"
    FIJO = "fijo"
    PORCENTAJE_SOBRE_PRECIO = "porcentaje_sobre_precio"
    GRUPO = "grupo"

class AmbitoUsoImpuestoEnum(str, Enum):
    BIENES = "bienes"
    SERVICIOS = "servicios"
    AMBOS = "ambos"

class CategoriaFiscalImpuestoEnum(str, Enum):
    AE = "AE - Cobro revertido del IVA"
    E = "E - Exención fiscal"
    S = "S - Tarifa estándar"
    Z = "Z - Bienes exentos"
    G = "G - Artículo de libre exportación"
    O = "O - Servicios fuera del alcance del IVA"
    K = "K - Exención del IVA"
    L = "L - Impuesto general indirecto de las Canarias"
    M = "M - Impuesto para producción, servicio e importación"
    B = "B - (IVA) transferido, en Italia"

class TipoArticuloEnum(str, Enum):
    PRODUCTO = "producto"
    SERVICIO = "servicio"
    CONSUMIBLE = "consumible"

class TipoDistribucionImpuestoEnum(str, Enum):
    FACTURA = "factura"
    REEMBOLSO = "reembolso"

class TipoReparticionBaseImpuestoEnum(str, Enum):
    BASE = "base"
    IMPUESTO = "impuesto"
