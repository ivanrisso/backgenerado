from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Boolean, Float, Date, DateTime, Text, Numeric
from typing import Optional, List
from decimal import Decimal
from datetime import date, datetime
from .base import Base

class CuentaCorriente(Base):
    __tablename__ = "cuentacorriente"
    id: Mapped[Optional[int]] = mapped_column()
    cliente_id: Mapped[int] = mapped_column()
    comprobante_id: Mapped[Optional[int]] = mapped_column()
    fecha: Mapped[date] = mapped_column()
    tipo: Mapped[str] = mapped_column()
    descripcion: Mapped[Optional[str]] = mapped_column()
    importe: Mapped[float] = mapped_column()
    signo: Mapped[int] = mapped_column()
    saldo: Mapped[Optional[float]] = mapped_column()
    cliente: Mapped[Cliente] = mapped_column()
    comprobante: Mapped[Optional[Comprobante]] = mapped_column()