from pydantic import BaseModel
from typing import Optional
from datetime import date

class ComprobanteCreate(BaseModel):
    cliente_id: int
    tipo_comprobante_id: int
    concepto_id: int
    tipo_doc_id: int
    moneda_id: int
    punto_venta: int
    numero: int
    fecha_emision: date
    doc_nro: str
    nombre_cliente: str
    cuit_cliente: str
    domicilio_cliente: str
    localidad_cliente: str
    cod_postal_cliente: str
    provincia_cliente: str
    cotizacion_moneda: float
    total_neto: float
    total_iva: float
    total_impuestos: float
    total: float
    observaciones: str

class ComprobanteUpdate(BaseModel):
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

class ComprobanteResponse(BaseModel):
    id: int
    cliente_id: int
    tipo_comprobante_id: int
    concepto_id: int
    tipo_doc_id: int
    moneda_id: int
    punto_venta: int
    numero: int
    fecha_emision: date
    doc_nro: str
    nombre_cliente: str
    cuit_cliente: str
    domicilio_cliente: str
    localidad_cliente: str
    cod_postal_cliente: str
    provincia_cliente: str
    cotizacion_moneda: float
    total_neto: float
    total_iva: float
    total_impuestos: float
    total: float
    observaciones: str

    class Config:
        from_attributes = True