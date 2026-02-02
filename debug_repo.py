import asyncio
import traceback
from app.infrastructure.db.engine import SessionLocal
from app.repositories.condiciontributaria_repository import CondicionTributariaRepositoryImpl

async def main():
    async with SessionLocal() as session:
        print("Testing CondicionTributariaRepository.get_all()...")
        repo = CondicionTributariaRepositoryImpl(session)
        try:
            results = await repo.get_all()
            print(f"Success! Got {len(results)} items.")
            for item in results:
                print(item)
        except Exception:
            print("CRASHED!")
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
