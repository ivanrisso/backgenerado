# app/schemas/comprobante_full.py
from pydantic import BaseModel
from typing import List, Optional

from .comprobante import ComprobanteCreate, ComprobanteResponse
from .comprobante_detalle import ComprobanteDetalleCreate, ComprobanteDetalleResponse
from .comprobante_impuesto import ComprobanteImpuestoCreate, ComprobanteImpuestoResponse
from app.domain.entities.comprobante_full import ComprobanteFull


class CbteAsoc(BaseModel):
    Tipo: int
    PtoVta: int
    Nro: int
    importe_imputar: Optional[float] = 0.0

class ComprobanteFullCreate(ComprobanteCreate):
    detalles: List[ComprobanteDetalleCreate]
    impuestos: List[ComprobanteImpuestoCreate]
    cbtes_asociados: Optional[List[CbteAsoc]] = []

class ComprobanteFullResponse(ComprobanteResponse):
    detalles: List[ComprobanteDetalleResponse]
    impuestos: List[ComprobanteImpuestoResponse]

    @classmethod
    def from_domain(cls, full: "ComprobanteFull") -> "ComprobanteFullResponse":
        return cls(
            **full.cabecera.__dict__,
            detalles=[
                ComprobanteDetalleResponse(**d.__dict__) for d in full.detalles
            ],
            impuestos=[
                ComprobanteImpuestoResponse(**i.__dict__) for i in full.impuestos
            ]
        )
