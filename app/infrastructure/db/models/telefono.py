from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Boolean, Float, Date, DateTime, Text, Numeric
from typing import Optional, List
from decimal import Decimal
from datetime import date, datetime
from .base import Base

class Telefono(Base):
    __tablename__ = "telefono"
    id: Mapped[Optional[int]] = mapped_column()
    tipo_tel_id: Mapped[int] = mapped_column()
    prefijo: Mapped[str] = mapped_column()
    numero: Mapped[str] = mapped_column()
    domicilio_id: Mapped[int] = mapped_column()
    tipo_tel: Mapped[TipoTel] = mapped_column()
    domicilio: Mapped[Domicilio] = mapped_column()