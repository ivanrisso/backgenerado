from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Boolean, Float, Date, DateTime, Text, Numeric
from typing import Optional, List
from decimal import Decimal
from datetime import date, datetime
from .base import Base

class Pais(Base):
    __tablename__ = "pais"
    id: Mapped[Optional[int]] = mapped_column()
    codigo: Mapped[str] = mapped_column()
    nombre: Mapped[str] = mapped_column()
    provincias: Mapped[List[""Provincia""]] = relationship(back_populates="pais")