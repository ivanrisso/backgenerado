from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Boolean, Float, Date, DateTime, Text, Numeric
from typing import Optional, List
from decimal import Decimal
from datetime import date, datetime
from .base import Base

class RolesUsuario(Base):
    __tablename__ = "rolesusuario"
    usuario_id: Mapped[int] = mapped_column()
    rol_id: Mapped[int] = mapped_column()