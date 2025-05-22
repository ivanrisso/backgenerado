from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Boolean, Float, Date, DateTime, Text, Numeric
from typing import Optional, List
from decimal import Decimal
from datetime import date, datetime
from .base import Base

class Provincia(Base):
    __tablename__ = "provincia"
    id: Mapped[Optional[int]] = mapped_column()
    provincia_nombre: Mapped["str"] = relationship(back_populates="provincia")
    pais_id: Mapped[int] = mapped_column()
    pais: Mapped[Pais] = mapped_column()
    localidades: Mapped[List[""Localidad""]] = relationship(back_populates="provincia")