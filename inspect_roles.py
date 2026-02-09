import asyncio
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.infrastructure.db.engine import SessionLocal
from app.infrastructure.db.orm_models import Usuario, Rol, MenuItem, RolMenuItem

async def inspect():
    async with SessionLocal() as session:
        # 1. Check User Role
        result = await session.execute(
            select(Usuario)
            .options(selectinload(Usuario.roles))
            .where(Usuario.usuario_email == "newtester@gmail.com")
        )
        user = result.scalar_one_or_none()
        if user:
            print(f"User: {user.usuario_email}, ID: {user.id}")
            print(f"Roles: {[r.rol_nombre for r in user.roles]}")
            role_ids = [r.id for r in user.roles]
        else:
            print("User newtester not found")
            return

        # 2. Check All Roles
        result = await session.execute(select(Rol))
        roles = result.scalars().all()
        print("\nAll Roles:")
        for r in roles:
            print(f"- {r.rol_nombre} (ID: {r.id})")

        # 3. Check All Menu Items
        result = await session.execute(select(MenuItem))
        menus = result.scalars().all()
        print("\nAll Menu Items:")
        for m in menus:
            print(f"- {m.nombre} (ID: {m.id}, Path: {m.path}, ParentID: {m.parent_id})")

        # 4. Check RolMenuItem for Existing Roles (1: admin, 2: nuevo rol, 3: Operador)
        target_role_ids = [1, 2, 3]
        print(f"\nMenu Items for Roles {target_role_ids}:")
        
        for r_id in target_role_ids:
            print(f"\nRole ID {r_id}:")
            stmt = (
                select(MenuItem)
                .join(RolMenuItem, MenuItem.id == RolMenuItem.menu_item_id)
                .where(RolMenuItem.rol_id == r_id)
            )
            result = await session.execute(stmt)
            my_menus = result.scalars().all()
            if not my_menus:
                 print("  (No menu items assigned)")
            for m in my_menus:
                 print(f"  - {m.nombre} (Path: {m.path})")

if __name__ == "__main__":
    asyncio.run(inspect())
