from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Boolean, Float, Date, DateTime, Text, Numeric
from typing import Optional, List
from decimal import Decimal
from datetime import date, datetime
from .base import Base

class MenuItem(Base):
    __tablename__ = "menuitem"
    id: Mapped[Optional[int]] = mapped_column()
    nombre: Mapped[str] = mapped_column()
    path: Mapped[Optional[str]] = mapped_column()
    parent_id: Mapped[Optional[int]] = mapped_column()
    orden: Mapped[int] = mapped_column(default=0)
    children: Mapped[List["MenuItem"]] = relationship(back_populates="menuitem")
    parent: Mapped[Optional["MenuItem"]] = mapped_column()
    roles: Mapped[List["Rol"]] = relationship(back_populates="menuitem")