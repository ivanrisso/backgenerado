import asyncio
from sqlalchemy import select
from app.infrastructure.db.engine import SessionLocal
from app.infrastructure.db.orm_models import MenuItem

async def list_menus():
    async with SessionLocal() as session:
        result = await session.execute(select(MenuItem))
        items = result.scalars().all()
        print(f"Total Items: {len(items)}")
        for item in items:
            print(f"ID: {item.id} | Nombre: '{item.nombre}' | Path: '{item.path}' | Parent: {item.parent_id}")

if __name__ == "__main__":
    asyncio.run(list_menus())
