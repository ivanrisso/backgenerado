from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Boolean, Float, Date, DateTime, Text, Numeric
from typing import Optional, List
from decimal import Decimal
from datetime import date, datetime
from .base import Base

class Localidad(Base):
    __tablename__ = "localidad"
    id: Mapped[Optional[int]] = mapped_column()
    localidad_nombre: Mapped["str"] = relationship(back_populates="localidad")
    cod_postal: Mapped[str] = mapped_column()
    provincia_id: Mapped[int] = mapped_column()
    provincia: Mapped[Provincia] = mapped_column()
    domicilios: Mapped[List[""Domicilio""]] = relationship(back_populates="localidad")