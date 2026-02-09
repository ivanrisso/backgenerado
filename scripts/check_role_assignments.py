
import sys
import asyncio
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, ForeignKey, String

sys.path.append('/home/irisso/proyectos/facturacion')

Base = declarative_base()

class RolMenuItem(Base):
    __tablename__ = "rolmenuitem"
    rol_id = Column(Integer, ForeignKey("rol.id"), primary_key=True)
    menu_item_id = Column(Integer, ForeignKey("menuitem.id"), primary_key=True)

class Rol(Base):
    __tablename__ = "rol"
    id = Column(Integer, primary_key=True)
    rol_nombre = Column(String)

DATABASE_URL = "mysql+asyncmy://app:app@localhost:3306/facturacion"
engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def check_roles():
    async with SessionLocal() as session:
        # Check if ID 22 is assigned to Admin
        # First get Admin Role ID
        stmt_rol = select(Rol).where(Rol.rol_nombre == "Admin")
        result_rol = await session.execute(stmt_rol)
        role = result_rol.scalar_one_or_none()
        
        if not role:
            print("Role Admin not found")
            return

        print(f"Admin Role ID: {role.id}")

        items_to_check = [28, 31, 32] # Cuenta Corriente, Tesorería, Recibos
        stmt = select(RolMenuItem).where(
            and_(
                RolMenuItem.rol_id == role.id,
                RolMenuItem.menu_item_id.in_(items_to_check)
            )
        )
        result = await session.execute(stmt)
        assigned = result.scalars().all()
        
        assigned_ids = [a.menu_item_id for a in assigned]
        print(f"Assigned Items to Admin: {assigned_ids}")
        
        for i in items_to_check:
            if i not in assigned_ids:
                print(f"WARNING: Item {i} is NOT assigned to Admin.")

if __name__ == "__main__":
    from sqlalchemy import String # Import missing
    asyncio.run(check_roles())
