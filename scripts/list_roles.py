import asyncio
import sys
from sqlalchemy import select

# Add app to path
import os
sys.path.append(os.getcwd())

from app.infrastructure.db.engine import SessionLocal
from app.infrastructure.db.orm_models import Rol

async def list_roles():
    async with SessionLocal() as session:
        result = await session.execute(select(Rol))
        roles = result.scalars().all()
        print("Available Roles:")
        for r in roles:
            print(f"- {r.rol_nombre} (ID: {r.id})")

if __name__ == "__main__":
    asyncio.run(list_roles())
