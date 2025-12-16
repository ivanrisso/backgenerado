import asyncio
from app.infrastructure.db.engine import SessionLocal
from app.services.auth_service import AuthService
from app.infrastructure.security.password_hashing import hash_password
from sqlalchemy import select
from app.infrastructure.db.orm_models import Usuario

async def reset_password():
    async with SessionLocal() as db:
        stmt = select(Usuario).where(Usuario.usuario_email == "admin@facturacion.com")
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if user:
            print(f"Usuario encontrado: {user.usuario_email}")
            print("Reseteando contraseña a 'admin123'...")
            user.usuario_password = hash_password("admin123")
            db.add(user)
            await db.commit()
            print("Contraseña actualizada correctamente.")
        else:
            print("Usuario no encontrado.")

if __name__ == "__main__":
    asyncio.run(reset_password())
