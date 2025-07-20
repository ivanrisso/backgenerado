# app/domain/entities/comprobanteimpuesto.py
from typing import Optional
from dataclasses import dataclass
from app.domain.dtos.comprobante_impuesto_dto import ComprobanteImpuestoDTO


@dataclass
class ComprobanteImpuesto:
    id: Optional[int] = None
    comprobante_id: Optional[int] = None
    tipo_impuesto_id: Optional[int] = None
    descripcion: Optional[str] = None
    base_imponible: Optional[float] = None
    alicuota: Optional[float] = None
    importe: Optional[float] = None

    @classmethod
    def from_dto(cls, dto: ComprobanteImpuestoDTO) -> "ComprobanteImpuesto":
        return cls(
            id=dto.id,
            comprobante_id=dto.comprobante_id,
            tipo_impuesto_id=dto.tipo_impuesto_id,
            descripcion=dto.descripcion,
            base_imponible=dto.base_imponible,
            alicuota=dto.alicuota,
            importe=dto.importe,
        )
