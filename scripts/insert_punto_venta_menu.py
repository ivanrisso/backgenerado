import asyncio
from sqlalchemy import select
from app.infrastructure.db.engine import SessionLocal
from app.infrastructure.db.orm_models import MenuItem, Rol, RolMenuItem

async def insert_punto_venta():
    async with SessionLocal() as session:
        print("Starting Menu Insertion for 'Puntos de Venta'...")

        # 1. Use Parent ID 3 (Configuración/Maestros)
        # Based on list_menu_items.py, Monedas/Operadores are under ID 3.
        parent_id = 3
        print(f"Using Parent ID: {parent_id} (Configuración/Maestros)")

        # 2. Check if 'Puntos de Venta' exists
        result = await session.execute(select(MenuItem).where(MenuItem.path == "/puntos-venta"))
        pv_menu = result.scalar_one_or_none()

        if pv_menu:
            print(f"Menu 'Puntos de Venta' already exists with ID: {pv_menu.id}")
        else:
            print("Creating 'Puntos de Venta' menu item...")
            pv_menu = MenuItem(
                nombre="Puntos de Venta",
                path="/puntos-venta",
                parent_id=parent_id
            )
            session.add(pv_menu)
            await session.commit()
            await session.refresh(pv_menu)
            print(f"Created 'Puntos de Venta' with ID: {pv_menu.id}")

        # 3. Assign to Admin Role
        result = await session.execute(select(Rol).where(Rol.rol_nombre == "Admin"))
        admin_role = result.scalar_one_or_none()
        
        if admin_role:
            # Check permission
            result = await session.execute(
                select(RolMenuItem).where(
                    (RolMenuItem.rol_id == admin_role.id) & 
                    (RolMenuItem.menu_item_id == pv_menu.id)
                )
            )
            perm = result.scalar_one_or_none()
            
            if not perm:
                print("Assigning permission to Admin...")
                session.add(RolMenuItem(rol_id=admin_role.id, menu_item_id=pv_menu.id))
                await session.commit()
            else:
                print("Admin already has permission.")
        
        print("Done.")

if __name__ == "__main__":
    asyncio.run(insert_punto_venta())
