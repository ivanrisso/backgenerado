import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from app.infrastructure.db.engine import SessionLocal
from app.infrastructure.db.orm_models import MenuItem
from sqlalchemy import select

from app.repositories.menuitem_repository import MenuItemRepositoryImpl
from app.infrastructure.db.orm_models import Rol

async def verify_orm():
    print("Verifying Repository...")
    async with SessionLocal() as session:
        try:
            repo = MenuItemRepositoryImpl(session)
            # Fetch all to test _to_domain
            items = await repo.get_all()
            print(f"Fetched {len(items)} items.")
            if items:
                print(f"First Item Orden: {items[0].orden}")
            else:
                print("No items.")
                
        except Exception as e:
            print(f"Repository Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(verify_orm())
