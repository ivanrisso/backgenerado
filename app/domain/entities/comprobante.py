# app/domain/entities/comprobante.py

from typing import Optional
from datetime import date
from dataclasses import dataclass
from app.domain.dtos.comprobante_dto import ComprobanteDTO

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
    cotizacion_moneda: Optional[float] = None
    total_neto: Optional[float] = None
    total_iva: Optional[float] = None
    total_impuestos: Optional[float] = None
    total: Optional[float] = None
    observaciones: Optional[str] = None
    cae: Optional[str] = None
    cae_vencimiento: Optional[date] = None
    saldo: Optional[float] = None

    @classmethod
    def from_dto(cls, dto: ComprobanteDTO) -> "Comprobante":
        return cls(
            cliente_id=dto.cliente_id,
            tipo_comprobante_id=dto.tipo_comprobante_id,
            concepto_id=dto.concepto_id,
            tipo_doc_id=dto.tipo_doc_id,
            moneda_id=dto.moneda_id,
            punto_venta=dto.punto_venta,
            fecha_emision=dto.fecha_emision,
            doc_nro=dto.doc_nro,
            nombre_cliente=dto.nombre_cliente,
            cuit_cliente=dto.cuit_cliente,
            domicilio_cliente=dto.domicilio_cliente,
            localidad_cliente=dto.localidad_cliente,
            cod_postal_cliente=dto.cod_postal_cliente,
            provincia_cliente=dto.provincia_cliente,
            cotizacion_moneda=dto.cotizacion_moneda,
            total_neto=dto.total_neto,
            total_iva=dto.total_iva,
            total_impuestos=dto.total_impuestos,
            total=dto.total,
            observaciones=dto.observaciones,
            saldo=dto.total # Default balance is full amount
        )
