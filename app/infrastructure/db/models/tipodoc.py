from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Boolean, Float, Date, DateTime, Text, Numeric
from typing import Optional, List
from decimal import Decimal
from datetime import date, datetime
from .base import Base

class TipoDoc(Base):
    __tablename__ = "tipodoc"
    id: Mapped[Optional[int]] = mapped_column()
    tipo_doc_nombre: Mapped[str] = mapped_column()
    habilitado: Mapped[bool] = mapped_column()
    comprobantes: Mapped[List[""Comprobante""]] = relationship(back_populates="tipodoc")
    clientes: Mapped[List[""Cliente""]] = relationship(back_populates="tipodoc")