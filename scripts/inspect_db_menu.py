
import sys
import os
import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

# Add project root
sys.path.append('/home/irisso/proyectos/facturacion')

# Define Minimal Model
Base = declarative_base()

class MenuItem(Base):
    __tablename__ = "menuitem"
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    path = Column(String)
    parent_id = Column(Integer, ForeignKey("menuitem.id"))
    orden = Column(Integer, default=0)
# Db Config
DATABASE_URL = "mysql+asyncmy://app:app@localhost:3306/facturacion"
engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def inspect_menu():
    async with SessionLocal() as session:
        stmt = select(MenuItem).order_by(MenuItem.id)
        result = await session.execute(stmt)
        items = result.scalars().all()
        
        print(f"{'ID':<5} | {'Nombre':<20} | {'Path':<30} | {'Parent':<5} | {'Orden':<5}")
        print("-" * 80)
        for item in items:
            p_path = item.path if item.path else "None"
            p_parent = str(item.parent_id) if item.parent_id is not None else "None"
            p_orden = str(item.orden) if hasattr(item, 'orden') else "N/A"
            print(f"{item.id:<5} | {item.nombre:<20} | {p_path:<30} | {p_parent:<5} | {p_orden:<5}")

if __name__ == "__main__":
    asyncio.run(inspect_menu())
