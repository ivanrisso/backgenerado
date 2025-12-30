
import asyncio
from app.infrastructure.db.engine import SessionLocal
from app.infrastructure.db.orm_models import Moneda
from sqlalchemy import select

async def check_moneda():
    async with SessionLocal() as session:
        result = await session.execute(select(Moneda))
        items = result.scalars().all()
        print(f"{'ID':<5} | {'DESCRIPCION':<20} | {'CODIGO (AFIP?)':<15} | {'CODIGO_ARCA':<10}")
        print("-" * 55)
        for i in items:
            print(f"{i.id:<5} | {i.descripcion:<20} | {i.codigo:<15} | {i.codigo_arca:<10}")

if __name__ == "__main__":
    asyncio.run(check_moneda())
