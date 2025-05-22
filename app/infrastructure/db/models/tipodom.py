from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Boolean, Float, Date, DateTime, Text, Numeric
from typing import Optional, List
from decimal import Decimal
from datetime import date, datetime
from .base import Base

class TipoDom(Base):
    __tablename__ = "tipodom"
    id: Mapped[Optional[int]] = mapped_column()
    nombre: Mapped[str] = mapped_column()
    domicilios: Mapped[List[""Domicilio""]] = relationship(back_populates="tipodom")