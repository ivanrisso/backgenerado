import asyncio
from sqlalchemy import text
from app.infrastructure.db.engine import SessionLocal

async def check_counts():
    async with SessionLocal() as session:
        t1 = await session.execute(text("SELECT COUNT(*) FROM tipoimpuesto"))
        c1 = t1.scalar()
        t2 = await session.execute(text("SELECT COUNT(*) FROM condiciontributaria"))
        c2 = t2.scalar()
        print(f"TipoImpuesto count: {c1}")
        print(f"CondicionTributaria count: {c2}")

if __name__ == "__main__":
    asyncio.run(check_counts())
