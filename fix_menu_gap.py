import asyncio
from sqlalchemy import select, delete
from app.infrastructure.db.engine import SessionLocal
from app.infrastructure.db.orm_models import Usuario, Rol, MenuItem, RolMenuItem, RolesUsuario

async def fix_permissions():
    async with SessionLocal() as session:
        print("Starting Permissions Fix...")

        # 1. Create or Get Role 'Operador'
        result = await session.execute(select(Rol).where(Rol.rol_nombre == "Operador"))
        role_operador = result.scalar_one_or_none()
        
        if not role_operador:
            print("Creating role 'Operador'...")
            role_operador = Rol(rol_nombre="Operador", es_admin=False)
            session.add(role_operador)
            await session.commit()
            await session.refresh(role_operador)
        print(f"Role 'Operador' ID: {role_operador.id}")

        # 2. Define Menu Items to Assign
        # Dashboard (29), Tesorería (31), Recibos (32), Configuración (3), Clientes (16)
        target_menu_ids = [29, 31, 32, 3, 16]
        
        # 3. Assign Menu Items to Role
        # First check what exists to avoid dupes (though RolMenuItem usually PK specific, let's be safe)
        # We can just clear and re-add or add if missing. Best is add if missing.
        
        result = await session.execute(
            select(RolMenuItem).where(RolMenuItem.rol_id == role_operador.id)
        )
        existing_permissions = result.scalars().all()
        existing_menu_ids = [p.menu_item_id for p in existing_permissions]
        
        for mid in target_menu_ids:
            if mid not in existing_menu_ids:
                print(f"Assigning Menu ID {mid} to Operador")
                new_perm = RolMenuItem(rol_id=role_operador.id, menu_item_id=mid)
                session.add(new_perm)
        
        await session.commit()

        # 4. Assign Role to User 'newtester'
        result = await session.execute(select(Usuario).where(Usuario.usuario_email == "newtester@gmail.com"))
        user = result.scalar_one_or_none()
        
        if user:
            # Check if user has role
            result = await session.execute(
                select(RolesUsuario).where(
                    (RolesUsuario.usuario_id == user.id) & 
                    (RolesUsuario.rol_id == role_operador.id)
                )
            )
            has_role = result.scalar_one_or_none()
            
            if not has_role:
                print(f"Assigning Role Operador to User {user.usuario_email}")
                new_role_link = RolesUsuario(usuario_id=user.id, rol_id=role_operador.id)
                session.add(new_role_link)
                await session.commit()
            else:
                print(f"User {user.usuario_email} already has Role Operador")
        else:
            print("User newtester not found!")

        print("Fix Complete.")

if __name__ == "__main__":
    asyncio.run(fix_permissions())
