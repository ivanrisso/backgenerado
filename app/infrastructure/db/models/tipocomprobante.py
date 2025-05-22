from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Boolean, Float, Date, DateTime, Text, Numeric
from typing import Optional, List
from decimal import Decimal
from datetime import date, datetime
from .base import Base

class TipoComprobante(Base):
    __tablename__ = "tipocomprobante"
    id: Mapped[Optional[int]] = mapped_column()
    codigo: Mapped[str] = mapped_column()
    descripcion: Mapped[str] = mapped_column()
    es_fiscal: Mapped[bool] = mapped_column()
    comprobantes: Mapped[List[""Comprobante""]] = relationship(back_populates="tipocomprobante")