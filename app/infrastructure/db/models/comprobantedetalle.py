from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Boolean, Float, Date, DateTime, Text, Numeric
from typing import Optional, List
from decimal import Decimal
from datetime import date, datetime
from .base import Base

class ComprobanteDetalle(Base):
    __tablename__ = "comprobantedetalle"
    id: Mapped[Optional[int]] = mapped_column()
    comprobante_id: Mapped[int] = mapped_column()
    iva_id: Mapped[int] = mapped_column()
    descripcion: Mapped[str] = mapped_column()
    cantidad: Mapped[float] = mapped_column()
    precio_unitario: Mapped[float] = mapped_column()
    importe: Mapped[float] = mapped_column()
    alicuota_iva: Mapped[float] = mapped_column()
    importe_iva: Mapped[float] = mapped_column()
    comprobante: Mapped[Comprobante] = mapped_column()
    iva: Mapped[Iva] = mapped_column()