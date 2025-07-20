# app/domain/dtos/comprobante_dto.py

from typing import Optional
from datetime import date

class ComprobanteDTO:
    cliente_id: Optional[int]
    tipo_comprobante_id: Optional[int]
    concepto_id: Optional[int]
    tipo_doc_id: Optional[int]
    moneda_id: Optional[int]
    punto_venta: Optional[int]
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

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
