from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Boolean, Float, Date, DateTime, Text, Numeric
from typing import Optional, List
from decimal import Decimal
from datetime import date, datetime
from .base import Base

class Operador(Base):
    __tablename__ = "operador"
    id: Mapped[Optional[int]] = mapped_column()
    cliente_id: Mapped[int] = mapped_column()
    cliente: Mapped[Cliente] = mapped_column()