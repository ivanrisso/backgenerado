from typing import Optional, List
from datetime import date
from dataclasses import dataclass

@dataclass
class Comprobante:
    id: Optional[int] = None
    cliente_id: Optional[int] = None
    tipo_comprobante_id: Optional[int] = None
    concepto_id: Optional[int] = None
    tipo_doc_id: Optional[int] = None
    moneda_id: Optional[int] = None
    punto_venta: Optional[int] = None
    numero: Optional[int] = None
    fecha_emision: Optional[date] = None
    doc_nro: Optional[str] = None
    nombre_cliente: Optional[str] = None
    cuit_cliente: Optional[str] = None
    domicilio_cliente: Optional[str] = None
    localidad_cliente: Optional[str] = None
    cod_postal_cliente: Optional[str] = None
    provincia_cliente: Optional[str] = None
    cotizacion_moneda: Optional[float]
    total_neto: Optional[float] = None
    total_iva: Optional[float] = None
    total_impuestos: Optional[float] = None
    total: Optional[float] = None
    observaciones: Optional[str] = None
