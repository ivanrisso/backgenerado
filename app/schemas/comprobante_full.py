# app/schemas/comprobante_full.py
from pydantic import BaseModel
from typing import List
from .comprobante import ComprobanteCreate
from .comprobante_detalle import ComprobanteDetalleCreate
from .comprobante_impuesto import ComprobanteImpuestoCreate

class ComprobanteFullCreate(ComprobanteCreate):
    detalles: List[ComprobanteDetalleCreate]
    impuestos: List[ComprobanteImpuestoCreate]
