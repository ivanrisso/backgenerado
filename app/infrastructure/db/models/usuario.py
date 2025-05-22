from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Boolean, Float, Date, DateTime, Text, Numeric
from typing import Optional, List
from decimal import Decimal
from datetime import date, datetime
from .base import Base

class Usuario(Base):
    __tablename__ = "usuario"
    id: Mapped[Optional[int]] = mapped_column()
    usuario_email: Mapped["str"] = relationship(back_populates="usuario")
    usuario_password: Mapped["str"] = relationship(back_populates="usuario")
    nombre: Mapped[str] = mapped_column()
    apellido: Mapped[str] = mapped_column()
    roles: Mapped[List[""Rol""]] = relationship(back_populates="usuario")
    auditorias: Mapped[List[""AuditoriaComprobante""]] = relationship(back_populates="usuario")
    plain_password: Mapped[str) -> bool:] = mapped_column()
    plain_password: Mapped[str):] = mapped_column()