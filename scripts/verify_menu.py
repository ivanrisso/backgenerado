import asyncio
import sys
from sqlalchemy import select
from sqlalchemy.orm import selectinload

# Add app to path
import os
sys.path.append(os.getcwd())

from app.infrastructure.db.engine import SessionLocal
from app.infrastructure.db.orm_models import MenuItem, Rol

async def verify_integrity():
    async with SessionLocal() as session:
        print("--- Verifying Menu Integrity ---")
        
        # 1. Check Tesorería
        tesoreria = (await session.execute(
            select(MenuItem)
            .where(MenuItem.nombre.ilike("%Tesorer%"))
            .options(selectinload(MenuItem.roles), selectinload(MenuItem.children))
        )).scalar_one_or_none()
        
        if not tesoreria:
            print("ERROR: Tesorería not found in DB.")
            return
            
        print(f"Parent: {tesoreria.nombre} (ID: {tesoreria.id})")
        print(f"- Path: {tesoreria.path}")
        print(f"- ParentID: {tesoreria.parent_id}")
        print(f"- Roles: {[r.rol_nombre for r in tesoreria.roles]}")
        
        # 2. Check Recibos
        recibos = next((c for c in tesoreria.children if c.nombre == "Recibos"), None)
        if not recibos:
             print("ERROR: Child 'Recibos' not found under Tesorería.")
             # Try global search
             recibos_global = (await session.execute(select(MenuItem).where(MenuItem.nombre == "Recibos"))).scalar_one_or_none()
             if recibos_global:
                 print(f"WARN: 'Recibos' found globally but not child. ParentID: {recibos_global.parent_id}")
        else:
             # Need to fetch roles for child (lazy load might not have them deep?)
             recibos_full = (await session.execute(
                select(MenuItem)
                .where(MenuItem.id == recibos.id)
                .options(selectinload(MenuItem.roles))
             )).scalar_one()
             
             print(f"Child: {recibos_full.nombre} (ID: {recibos_full.id})")
             print(f"- Path: {recibos_full.path}")
             print(f"- Roles: {[r.rol_nombre for r in recibos_full.roles]}")

        # 3. Check Admin User Role
        # Assuming user is using 'admin' or email 'admin@example.com' or similar
        # Just listing users with 'admin' role
        admin_role = (await session.execute(select(Rol).where(Rol.rol_nombre == "admin"))).scalar_one_or_none()
        if admin_role:
             stmt_users = select(Rol).where(Rol.id == admin_role.id).options(selectinload(Rol.usuarios))
             admin_role_loaded = (await session.execute(stmt_users)).scalar_one()
             print(f"Users with 'admin' role: {[u.usuario_email for u in admin_role_loaded.usuarios]}")

if __name__ == "__main__":
    asyncio.run(verify_integrity())
