import asyncio
import sys
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

# Add app to path
import os
sys.path.append(os.getcwd())

from app.infrastructure.db.engine import SessionLocal
from app.infrastructure.db.orm_models import MenuItem, Rol

async def fix_menu():
    async with SessionLocal() as session:
        print("Searching for 'Tesorería' parent menu...")
        
        # 1. Debug: List all root items
        stmt = select(MenuItem).where(MenuItem.parent_id.is_(None))
        roots = (await session.execute(stmt)).scalars().all()
        print("Root Menu Items found:")
        for r in roots:
            print(f"- {r.nombre} (ID: {r.id})")

        # 1. Find or Create 'Tesorería' Parent
        stmt = select(MenuItem).where(MenuItem.nombre.ilike("%Tesorer%")).options(selectinload(MenuItem.children))
        result = await session.execute(stmt)
        tesoreria = result.scalar_one_or_none()
        
        if not tesoreria:
            print("Parent menu 'Tesorería' not found. Creating it...")
            tesoreria = MenuItem(
                nombre="Tesorería",
                path=None, # Root often has no path or a dummy one
                parent_id=None
            )
            session.add(tesoreria)
            await session.flush()
            print(f"Created 'Tesorería' (ID: {tesoreria.id})")
        else:
            print(f"Found Parent: {tesoreria.nombre} (ID: {tesoreria.id})")

        # 2. Find and Delete 'Nuevo Recibo' GLOBALLY (regardless of parent)
        stmt_del = select(MenuItem).where(MenuItem.nombre.ilike("%Nuevo Recibo%"))
        items_to_del = (await session.execute(stmt_del)).scalars().all()
        
        for item in items_to_del:
            print(f"Removing old item: {item.nombre} (ID: {item.id}, Parent: {item.parent_id})")
            await session.delete(item)
            
        # 3. Create or Update 'Recibos'
        # Check if it already exists under Tesorería
        # Need to refresh children or query directly
        stmt_recibos = select(MenuItem).where(MenuItem.parent_id == tesoreria.id, MenuItem.nombre == "Recibos")
        recibos_item = (await session.execute(stmt_recibos)).scalar_one_or_none()
        
        if not recibos_item:
            print("Creating 'Recibos' menu item...")
            recibos_item = MenuItem(
                nombre="Recibos",
                path="/recibos",
                parent_id=tesoreria.id
            )
            session.add(recibos_item)
            await session.flush()
            print(f"Created 'Recibos' (ID: {recibos_item.id})")
        else:
            print(f"Updating 'Recibos' (ID: {recibos_item.id}) path...")
            recibos_item.path = "/recibos"
            session.add(recibos_item)

        # 4. Assign Roles (admin)
        # Fetch Admin role
        admin_rol = (await session.execute(select(Rol).where(Rol.rol_nombre == "admin"))).scalar_one_or_none()
        
        if admin_rol:
            # Re-fetch item with roles
            stmt_reload = select(MenuItem).where(MenuItem.id == recibos_item.id).options(selectinload(MenuItem.roles))
            recibos_reloaded = (await session.execute(stmt_reload)).scalar_one()
            
            if admin_rol not in recibos_reloaded.roles:
                print("Assigning 'admin' role to Recibos...")
                recibos_reloaded.roles.append(admin_rol)
            else:
                print("Role 'admin' already assigned to Recibos.")
                
            # Also assign to Parent 'Tesorería' just in case
            stmt_parent = select(MenuItem).where(MenuItem.id == tesoreria.id).options(selectinload(MenuItem.roles))
            tesoreria_reloaded = (await session.execute(stmt_parent)).scalar_one()
            
            if admin_rol not in tesoreria_reloaded.roles:
                print("Assigning 'admin' role to Tesorería...")
                tesoreria_reloaded.roles.append(admin_rol)
        else:
            print("WARNING: Role 'admin' not found.")

        await session.commit()
        print("Menu fix completed successfully.")

if __name__ == "__main__":
    asyncio.run(fix_menu())
