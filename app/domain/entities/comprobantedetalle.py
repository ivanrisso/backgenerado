# app/domain/entities/comprobantedetalle.py
from typing import Optional
from dataclasses import dataclass
from app.domain.dtos.comprobante_detalle_dto import ComprobanteDetalleDTO


@dataclass
class ComprobanteDetalle:
    id: Optional[int] = None
    comprobante_id: Optional[int] = None
    iva_id: Optional[int] = None
    descripcion: Optional[str] = None
    cantidad: Optional[float] = None
    precio_unitario: Optional[float] = None
    importe: Optional[float] = None
    alicuota_iva: Optional[float] = None
    alicuota_iva: Optional[float] = None
    importe_iva: Optional[float] = None
    datos_extra: Optional[dict] = None

    @classmethod
    def from_dto(cls, dto: ComprobanteDetalleDTO) -> "ComprobanteDetalle":
        return cls(
            id=dto.id,
            comprobante_id=dto.comprobante_id,
            iva_id=dto.iva_id,
            descripcion=dto.descripcion,
            cantidad=dto.cantidad,
            precio_unitario=dto.precio_unitario,
            importe=dto.importe,
            alicuota_iva=dto.alicuota_iva,
            importe_iva=dto.importe_iva,
            datos_extra=getattr(dto, 'datos_extra', None)
        )
