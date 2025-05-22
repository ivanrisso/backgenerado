from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Boolean, Float, Date, DateTime, Text, Numeric
from typing import Optional, List
from decimal import Decimal
from datetime import date, datetime
from .base import Base

class TipoTel(Base):
    __tablename__ = "tipotel"
    id: Mapped[Optional[int]] = mapped_column()
    nombre: Mapped[str] = mapped_column()
    telefonos: Mapped[List[""Telefono""]] = relationship(back_populates="tipotel")