from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class ComprobanteBase(BaseModel):
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
    cod_postal_cliente: Optional[str]
    provincia_cliente: str
    cotizacion_moneda: float
    total_neto: float
    total_iva: float
    total_impuestos: float
    total: float
    observaciones: Optional[str]

class ComprobanteCreate(ComprobanteBase):
    pass

class ComprobanteResponse(ComprobanteBase):
    id: int

    class Config:
        from_attributes = True