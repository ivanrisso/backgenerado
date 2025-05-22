from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Boolean, Float, Date, DateTime, Text, Numeric
from typing import Optional, List
from decimal import Decimal
from datetime import date, datetime
from .base import Base

class Rol(Base):
    __tablename__ = "rol"
    id: Mapped[Optional[int]] = mapped_column()
    rol_nombre: Mapped["str"] = relationship(back_populates="rol")
    es_admin: Mapped[bool] = mapped_column()
    usuarios: Mapped[List["Usuario"]] = relationship(back_populates="rol")
    menuitems: Mapped[List[""MenuItem""]] = relationship(back_populates="rol")