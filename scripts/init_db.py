import asyncio
import logging
from app.infrastructure.db.engine import create_db_and_tables

# Init logger to see output
logging.basicConfig(level=logging.INFO)

async def main():
    print("Starting DB Init...")
    await create_db_and_tables()
    print("DB Init Complete.")

if __name__ == "__main__":
    asyncio.run(main())
