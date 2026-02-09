import asyncio
from sqlalchemy import select
from app.infrastructure.db.engine import SessionLocal
from app.infrastructure.db.orm_models import MenuItem, Rol, RolMenuItem

async def fix_menu():
    print("Iniciando reparación de Menú Seguridad...")
    async with SessionLocal() as session:
        try:
            # 1. Verificar si existe ID 4
            stmt = select(MenuItem).where(MenuItem.id == 4)
            result = await session.execute(stmt)
            existing_item = result.scalar_one_or_none()

            if existing_item:
                print(f"El item ID 4 ya existe: {existing_item.nombre}. Verificando rol...")
                menu_item = existing_item
            else:
                # 2. Insertar Item ID 4
                print("Insertando Menu Item ID 4 (Seguridad)...")
                menu_item = MenuItem(
                    id=4,
                    nombre="Seguridad",
                    path=None,   # Es un grupo
                    parent_id=None
                )
                session.add(menu_item)
                await session.flush() # Para asegurar que esté disponible para relaciones
                print("Item insertado.")

            # 3. Buscar Rol Admin
            stmt_rol = select(Rol).where(Rol.rol_nombre == "Admin")
            result_rol = await session.execute(stmt_rol)
            rol_admin = result_rol.scalar_one_or_none()

            if not rol_admin:
                print("ERROR: No se encontró el rol Admin.")
                return

            print(f"Rol Admin encontrado (ID: {rol_admin.id}).")

            # 4. Verificar asignación
            stmt_assoc = select(RolMenuItem).where(
                RolMenuItem.rol_id == rol_admin.id,
                RolMenuItem.menu_item_id == 4
            )
            result_assoc = await session.execute(stmt_assoc)
            assoc = result_assoc.scalar_one_or_none()

            if assoc:
                print("La asignación Rol-Menu ya existe.")
            else:
                print("Creando asignación Rol-Menu...")
                new_assoc = RolMenuItem(rol_id=rol_admin.id, menu_item_id=4)
                session.add(new_assoc)
                print("Asignación creada.")

            await session.commit()
            print("Reparación completada exitosamente.")

        except Exception as e:
            await session.rollback()
            print(f"Error durante la reparación: {e}")
            raise

if __name__ == "__main__":
    asyncio.run(fix_menu())
