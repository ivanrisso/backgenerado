from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Boolean, Float, Date, DateTime, Text, Numeric
from typing import Optional, List
from decimal import Decimal
from datetime import date, datetime
from .base import Base

class Domicilio(Base):
    __tablename__ = "domicilio"
    id: Mapped[Optional[int]] = mapped_column()
    calle: Mapped[str] = mapped_column()
    numero: Mapped[int] = mapped_column()
    cliente_id: Mapped[int] = mapped_column()
    tipo_dom_id: Mapped[int] = mapped_column()
    localidad_id: Mapped[int] = mapped_column()
    cliente: Mapped[Cliente] = mapped_column()
    tipo_dom: Mapped[TipoDom] = mapped_column()
    localidad: Mapped[Localidad] = mapped_column()
    telefonos: Mapped[List[""Telefono""]] = relationship(back_populates="domicilio")