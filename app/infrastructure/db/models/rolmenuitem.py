from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Boolean, Float, Date, DateTime, Text, Numeric
from typing import Optional, List
from decimal import Decimal
from datetime import date, datetime
from .base import Base

class RolMenuItem(Base):
    __tablename__ = "rolmenuitem"
    rol_id: Mapped[int] = mapped_column()
    menu_item_id: Mapped[int] = mapped_column()