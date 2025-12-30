
import asyncio
from app.infrastructure.db.engine import SessionLocal
from app.infrastructure.db.orm_models import Usuario
from app.infrastructure.security.password_hashing import hash_password
from sqlalchemy import select

async def reset():
    email = "admin@facturacion.com"
    new_pass = "admin123"
    
    async with SessionLocal() as session:
        result = await session.execute(select(Usuario).where(Usuario.usuario_email == email))
        user = result.scalar_one_or_none()
        
        hashed = hash_password(new_pass)
        
        if user:
            print(f"Usuario {email} encontrado. Actualizando password...")
            user.usuario_password = hashed
        else:
            print(f"Usuario {email} no encontrado. Creando usuario...")
            user = Usuario(
                usuario_email=email,
                usuario_password=hashed,
                nombre="Admin",
                apellido="Sistema"
            )
            session.add(user)
            
        await session.commit()
        print(f"Password reset exitoso. Nuevo password: {new_pass}")

if __name__ == "__main__":
    asyncio.run(reset())
