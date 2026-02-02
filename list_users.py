import asyncio
from sqlalchemy import select
from app.infrastructure.db.engine import SessionLocal
from app.infrastructure.db.orm_models import Usuario

async def list_users():
    async with SessionLocal() as session:
        result = await session.execute(select(Usuario))
        users = result.scalars().all()
        print(f"Found {len(users)} users:")
        for u in users:
            print(f"- {u.usuario_email} (ID: {u.id})")

if __name__ == "__main__":
    asyncio.run(list_users())
