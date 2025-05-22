from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Boolean, Float, Date, DateTime, Text, Numeric
from typing import Optional, List
from decimal import Decimal
from datetime import date, datetime
from .base import Base

class Comprobante(Base):
    __tablename__ = "comprobante"
    id: Mapped[Optional[int]] = mapped_column()
    cliente_id: Mapped[int] = mapped_column()
    tipo_comprobante_id: Mapped["int"] = relationship(back_populates="comprobante")
    concepto_id: Mapped[int] = mapped_column()
    tipo_doc_id: Mapped[int] = mapped_column()
    moneda_id: Mapped[int] = mapped_column()
    punto_venta: Mapped[int] = mapped_column()
    numero: Mapped[int] = mapped_column()
    fecha_emision: Mapped[date] = mapped_column()
    doc_nro: Mapped[str] = mapped_column()
    nombre_cliente: Mapped[str] = mapped_column()
    cuit_cliente: Mapped[str] = mapped_column()
    domicilio_cliente: Mapped[str] = mapped_column()
    localidad_cliente: Mapped[str] = mapped_column()
    cod_postal_cliente: Mapped[Optional[str]] = mapped_column()
    provincia_cliente: Mapped[str] = mapped_column()
    cotizacion_moneda: Mapped[float] = mapped_column()
    total_neto: Mapped[float] = mapped_column()
    total_iva: Mapped[float] = mapped_column()
    total_impuestos: Mapped[float] = mapped_column()
    total: Mapped[float] = mapped_column()
    observaciones: Mapped[Optional[str]] = mapped_column()
    tipo_comprobante: Mapped["TipoComprobante"] = relationship(back_populates="comprobante")
    concepto: Mapped[Concepto] = mapped_column()
    tipo_doc: Mapped[TipoDoc] = mapped_column()
    moneda: Mapped[Moneda] = mapped_column()
    cliente: Mapped[Cliente] = mapped_column()
    detalles: Mapped[List[""ComprobanteDetalle""]] = relationship(back_populates="comprobante")
    impuestos: Mapped[List[""ComprobanteImpuesto""]] = relationship(back_populates="comprobante")
    registro_cc: Mapped[Optional["CuentaCorriente"]] = mapped_column()
    auditorias: Mapped[List[""AuditoriaComprobante""]] = relationship(back_populates="comprobante")