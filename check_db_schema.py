import asyncio
from sqlalchemy import text
from app.infrastructure.db.engine import SessionLocal

async def check_schema():
    async with SessionLocal() as session:
        print("Checking Schema...")
        res = await session.execute(text("SHOW CREATE TABLE tipoimpuesto"))
        row = res.fetchone()
        print(row[1])

        res2 = await session.execute(text("SELECT id, categoria FROM tipoimpuesto LIMIT 5"))
        print("\nData Sample:")
        for r in res2:
            print(r)

if __name__ == "__main__":
    asyncio.run(check_schema())
