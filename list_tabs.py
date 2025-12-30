
import asyncio
from app.infrastructure.db.engine import SessionLocal
from sqlalchemy import text

async def list_tabs():
    async with SessionLocal() as db:
        res = await db.execute(text("SHOW TABLES"))
        tables = [r[0] for r in res.all()]
        print(f"Total Tables found: {len(tables)}")
        for t in sorted(tables):
            print(f"- {t}")

if __name__ == "__main__":
    asyncio.run(list_tabs())
