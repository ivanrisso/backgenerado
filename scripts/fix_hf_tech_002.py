
import sys
import asyncio
from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

# Add project root
sys.path.append('/home/irisso/proyectos/facturacion')

# Define Models
Base = declarative_base()

class MenuItem(Base):
    __tablename__ = "menuitem"
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    path = Column(String)

class RolMenuItem(Base):
    __tablename__ = "rolmenuitem"
    rol_id = Column(Integer, ForeignKey("rol.id"), primary_key=True)
    menu_item_id = Column(Integer, ForeignKey("menuitem.id"), primary_key=True)

# Db Config
DATABASE_URL = "mysql+asyncmy://app:app@localhost:3306/facturacion"
engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def apply_fix():
    print("Applying HF-TECH-002 Data Fix...")
    async with SessionLocal() as session:
        # 1. Fix Dashboard Path
        print("1. Updating Dashboard Path (ID 29) to '/'...")
        stmt_update = update(MenuItem).where(MenuItem.id == 29).values(path='/')
        await session.execute(stmt_update)
        
        # 2. Fix Orphan Comprobantes (Assign ID 22 to Role 1)
        print("2. Checking assignment of 'Comprobantes' (ID 22) to Admin (ID 1)...")
        stmt_check = select(RolMenuItem).where(RolMenuItem.rol_id == 1, RolMenuItem.menu_item_id == 22)
        result = await session.execute(stmt_check)
        exists = result.scalar_one_or_none()
        
        if not exists:
            print("   Assigning ID 22 to Admin...")
            stmt_insert = insert(RolMenuItem).values(rol_id=1, menu_item_id=22)
            await session.execute(stmt_insert)
        else:
            print("   ID 22 is already assigned to Admin.")

        await session.commit()
        print("HF-TECH-002 Success.")

if __name__ == "__main__":
    asyncio.run(apply_fix())
