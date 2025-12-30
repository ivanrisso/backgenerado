from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Boolean, Float, Date, DateTime, Text, Numeric
from typing import Optional, List
from decimal import Decimal
from datetime import date, datetime
from .base import Base

class Cliente(Base):
    __tablename__ = "cliente"
    id: Mapped[Optional[int]] = mapped_column()
    nombre: Mapped[str] = mapped_column()
    apellido: Mapped[str] = mapped_column()
    razon_social: Mapped[Optional[str]] = mapped_column()
    cuit: Mapped[Optional[str]] = mapped_column()
    email: Mapped[Optional[EmailStr]] = mapped_column()
    tipo_doc_id: Mapped[int] = mapped_column()
    iva_id: Mapped[int] = mapped_column()
    iva: Mapped["Iva"] = mapped_column()
    tipo_doc: Mapped[TipoDoc] = mapped_column()
    comprobantes: Mapped[List[""Comprobante""]] = relationship(back_populates="cliente")
    domicilios: Mapped[List[""Domicilio""]] = relationship(back_populates="cliente")

    movimientos_cc: Mapped[List[""CuentaCorriente""]] = relationship(back_populates="cliente")
    operadores: Mapped[List[""Operador""]] = relationship(back_populates="cliente")