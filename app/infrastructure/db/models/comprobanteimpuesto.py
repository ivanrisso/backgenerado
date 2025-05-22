from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Boolean, Float, Date, DateTime, Text, Numeric
from typing import Optional, List
from decimal import Decimal
from datetime import date, datetime
from .base import Base

class ComprobanteImpuesto(Base):
    __tablename__ = "comprobanteimpuesto"
    id: Mapped[Optional[int]] = mapped_column()
    comprobante_id: Mapped[int] = mapped_column()
    tipo_impuesto_id: Mapped[int] = mapped_column()
    descripcion: Mapped[str] = mapped_column()
    base_imponible: Mapped[float] = mapped_column()
    alicuota: Mapped[float] = mapped_column()
    importe: Mapped[float] = mapped_column()
    comprobante: Mapped[Comprobante] = mapped_column()
    tipo_impuesto: Mapped[TipoImpuesto] = mapped_column()