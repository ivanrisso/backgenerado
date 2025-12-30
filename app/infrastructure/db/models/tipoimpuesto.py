from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Boolean, Float, Date, DateTime, Text, Numeric
from typing import Optional, List
from decimal import Decimal
from datetime import date, datetime
from .base import Base

class TipoImpuesto(Base):
    __tablename__ = "tipoimpuesto"
    id: Mapped[Optional[int]] = mapped_column()
    codigo_afip: Mapped[str] = mapped_column()
    nombre: Mapped[str] = mapped_column()
    descripcion: Mapped[str] = mapped_column()
    tipo_aplicacion: Mapped[TipoAplicacionEnum] = mapped_column()
    base_calculo: Mapped[BaseTributarioEnum] = mapped_column()
    porcentaje: Mapped[Optional[float]] = mapped_column()
    editable: Mapped[bool] = mapped_column()
    obligatorio: Mapped[bool] = mapped_column()
    activo: Mapped[bool] = mapped_column()

    comprobantes: Mapped[List[""ComprobanteImpuesto""]] = relationship(back_populates="tipoimpuesto")