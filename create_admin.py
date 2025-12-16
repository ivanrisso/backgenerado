import asyncio
from app.infrastructure.db.engine import SessionLocal
from app.services.auth_service import AuthService
from app.schemas.auth_schemas import UsuarioCreate
from app.repositories.rol_repository import RolRepositoryImpl
from app.infrastructure.db.orm_models import Rol, Usuario

async def create_admin():
    async with SessionLocal() as db:
        auth_service = AuthService(db)
        rol_repo = RolRepositoryImpl(db)
        
        # 1. Asegurar rol admin
        rol_admin = await rol_repo.get_by_nombre("admin")
        if not rol_admin:
            print("Creando rol 'admin'...")
            rol_admin = Rol(rol_nombre="admin", es_admin=True)
            db.add(rol_admin)
            await db.commit()
            await db.refresh(rol_admin)
            # Re-convert to ORM object if using Repository that returns Domain Entity?
            # Actually RolRepositoryImpl returns Domain Entity. 
            # But to append to user.roles relationship (ORM), we need ORM object.
            # repository 'create' returns domain entity. 
            # We need to fetch ORM object or create it directly.
            # Let's just assume we need ORM object for relationship manipulation
            pass
            
        # To strictly use ORM for relationship assignment:
        # We need to get the ORM instance of the Role.
        from sqlalchemy import select
        from sqlalchemy.orm import selectinload
        stmt = select(Rol).where(Rol.rol_nombre == "admin")
        result = await db.execute(stmt)
        rol_orm = result.scalar_one()

        # 2. Crear usuario si no existe
        user_db = await auth_service.usuario_repo.get_by_email("admin@facturacion.com")
        if not user_db:
            print("Creando usuario admin...")
            try:
                await auth_service.registrar_usuario(UsuarioCreate(
                    usuario_email="admin@facturacion.com",
                    usuario_password="admin123",
                    nombre="Admin",
                    apellido="System"
                ))
            except Exception as e:
                print(f"Error creando usuario: {e}")
                return

        # 3. Asignar rol (Eager load roles for relationship check)
        stmt_user = select(Usuario).options(selectinload(Usuario.roles)).where(Usuario.usuario_email == "admin@facturacion.com")
        res_user = await db.execute(stmt_user)
        user_orm = res_user.scalar_one()
        
        # Check if role is present using ID to avoid object identity issues if session diff (should be same though)
        rol_ids = [r.id for r in user_orm.roles]
        if rol_orm.id not in rol_ids:
            print("Asignando rol admin al usuario...")
            user_orm.roles.append(rol_orm)
            await db.commit()
            await db.refresh(user_orm)

        # 4. Generar token
        # AuthService.crear_tokens takes 'usuario' which is expected to have 'usuario_email'
        # user_orm has it.
        token, _ = auth_service.crear_tokens(user_orm)
        print("\n========================================================")
        print("TOKEN DE ACCESO GENERADO:")
        print(token)
        print("========================================================")
        print("Instrucciones:")
        print("1. Abre la consola del navegador (F12 -> Console).")
        print(f"2. Ejecuta: localStorage.setItem('token', '{token}')")
        print("3. Recarga la página.")
        print("========================================================")

if __name__ == "__main__":
    asyncio.run(create_admin())
