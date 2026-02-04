
import asyncio
import sys
import os
sys.path.append(os.getcwd())
from app.infrastructure.db.engine import SessionLocal
from app.infrastructure.db.orm_models import Cliente, CondicionTributaria
from sqlalchemy import select
from sqlalchemy.orm import joinedload

async def list_clients():
    async with SessionLocal() as session:
        # List Conditions
        stmt_cond = select(CondicionTributaria)
        res_cond = await session.execute(stmt_cond)
        conds = res_cond.scalars().all()
        print(f"Total Conditions: {len(conds)}")
        ri_id = None
        for c in conds:
            print(f"Cond ID: {c.id} | Name: {c.nombre}")
            if "Inscripto" in c.nombre:
                ri_id = c.id
        
        if not ri_id and conds:
             ri_id = conds[0].id # Fallback
             
        stmt = select(Cliente).options(joinedload(Cliente.condicion_iva))
        result = await session.execute(stmt)
        clients = result.scalars().all()
        print(f"Total Clients: {len(clients)}")
        for c in clients:
            cond_name = c.condicion_iva.nombre if c.condicion_iva else "NONE"
            print(f"ID: {c.id} | Name: {c.nombre} | IVA_ID: {c.condicion_iva_id} | Cond: {cond_name}")
            
            # UPDATE IVAN (ID 3)
            if c.id == 3:
                print(f"UPDATING Client {c.id} to Condition {ri_id}")
                c.condicion_iva_id = ri_id
                session.add(c)
                await session.commit()
                print("UPDATE BUFFERED")

if __name__ == "__main__":
    asyncio.run(list_clients())
