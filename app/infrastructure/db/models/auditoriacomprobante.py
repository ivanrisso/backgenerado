from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Boolean, Float, Date, DateTime, Text, Numeric
from typing import Optional, List
from decimal import Decimal
from datetime import date, datetime
from .base import Base

class AuditoriaComprobante(Base):
    __tablename__ = "auditoriacomprobante"
    id: Mapped[Optional[int]] = mapped_column()
    comprobante_id: Mapped[int] = mapped_column()
    usuario_id: Mapped[int] = mapped_column()
    accion: Mapped[str] = mapped_column()
    detalle: Mapped[Optional[str]] = mapped_column()
    ip_origen: Mapped[Optional[str]] = mapped_column()
    fecha: Mapped[datetime] = mapped_column()
    comprobante: Mapped[Comprobante] = mapped_column()
    usuario: Mapped[Usuario] = mapped_column()