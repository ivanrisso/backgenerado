from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Boolean, Float, Date, DateTime, Text, Numeric
from typing import Optional, List
from decimal import Decimal
from datetime import date, datetime
from .base import Base

class ClienteImpuesto(Base):
    __tablename__ = "clienteimpuesto"
    id: Mapped[Optional[int]] = mapped_column()
    cliente_id: Mapped[int] = mapped_column()
    tipo_impuesto_id: Mapped[int] = mapped_column()
    aplica: Mapped[bool] = mapped_column()
    alicuota: Mapped[Optional[float]] = mapped_column()
    observaciones: Mapped[Optional[str]] = mapped_column()
    cliente: Mapped[Cliente] = mapped_column()
    tipo_impuesto: Mapped[TipoImpuesto] = mapped_column()