from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Boolean, Float, Date, DateTime, Text, Numeric
from typing import Optional, List
from decimal import Decimal
from datetime import date, datetime
from .base import Base

class Iva(Base):
    __tablename__ = "iva"
    id: Mapped[Optional[int]] = mapped_column()
    codigo: Mapped[int] = mapped_column()
    descripcion: Mapped[str] = mapped_column()
    porcentaje: Mapped[Decimal] = mapped_column()
    discriminado: Mapped[bool] = mapped_column()
    porcentaje_sobre: Mapped[Decimal] = mapped_column()
    clientes: Mapped[List["Cliente"]] = relationship(back_populates="iva")
    detalles: Mapped[List[""ComprobanteDetalle""]] = relationship(back_populates="iva")