
import asyncio
from app.infrastructure.db.engine import SessionLocal
from sqlalchemy import text

async def check():
    async with SessionLocal() as db:
        print("--- Checking tables ---")
        for table in ["tipoimpuesto", "iva", "condiciontributaria"]:
            try:
                res = await db.execute(text(f"SELECT count(*) FROM {table}"))
                count = res.scalar()
                print(f"Table '{table}': {count} rows")
                if count > 0:
                    res = await db.execute(text(f"SELECT * FROM {table} LIMIT 3"))
                    cols = res.keys()
                    rows = res.all()
                    print(f"  Columns: {list(cols)}")
                    for r in rows:
                        print(f"  Row: {dict(zip(cols, r))}")
            except Exception as e:
                print(f"Table '{table}' error: {e}")
        print("-----------------------")

if __name__ == "__main__":
    asyncio.run(check())
