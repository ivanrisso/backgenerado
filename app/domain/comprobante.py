from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, TYPE_CHECKING
from datetime import date
from app.domain.tipocomprobante import TipoComprobante
from app.domain.concepto import Concepto
from app.domain.tipodoc import TipoDoc
from app.domain.moneda import Moneda

if TYPE_CHECKING:
    from app.domain.cliente import Cliente
    from app.domain.comprobantedetalle import ComprobanteDetalle
    from app.domain.comprobanteimpuesto import ComprobanteImpuesto
    from app.domain.cuentacorriente import CuentaCorriente
    from app.domain.auditoriacomprobante import AuditoriaComprobante


@dataclass
class Comprobante:
    id: Optional[int]
    cliente_id: Optional[int]
    tipo_comprobante_id: Optional[int]
    concepto_id: Optional[int]
    tipo_doc_id: Optional[int]
    moneda_id: Optional[int]
    punto_venta: Optional[int]
    numero: Optional[int]
    fecha_emision: Optional[date]
    doc_nro: Optional[str]
    nombre_cliente: Optional[str]
    cuit_cliente: Optional[str]
    domicilio_cliente: Optional[str]
    localidad_cliente: Optional[str]
    cod_postal_cliente: Optional[str]
    provincia_cliente: Optional[str]
    cotizacion_moneda: Optional[float]
    total_neto: Optional[float]
    total_iva: Optional[float]
    total_impuestos: Optional[float]
    total: Optional[float]
    observaciones: Optional[str]
    tipo_comprobante: Optional[TipoComprobante]
    concepto: Optional[Concepto]
    tipo_doc: Optional[TipoDoc]
    moneda: Optional[Moneda]
    cliente: Optional["Cliente"]
    detalles: List["ComprobanteDetalle"]
    impuestos: List["ComprobanteImpuesto"]
    registro_cc: Optional["CuentaCorriente"]
    auditorias: List["AuditoriaComprobante"]