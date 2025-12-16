import asyncio
from typing import List
from app.infrastructure.db.engine import SessionLocal
from app.infrastructure.db.orm_models import Iva
from decimal import Decimal
from sqlalchemy import select

async def main():
    async with SessionLocal() as db:
        # Check if exists
        stmt = select(Iva)
        result = await db.execute(stmt)
        if result.scalars().first():
            print("IVA already seeded")
            return

        ivas = [
            Iva(id=1, codigo=1, descripcion="IVA Responsable Inscripto", porcentaje=Decimal("0.00"), discriminado=True, porcentaje_sobre=Decimal("0.00")),
            Iva(id=2, codigo=2, descripcion="IVA Responsable No Inscripto", porcentaje=Decimal("0.00"), discriminado=True, porcentaje_sobre=Decimal("0.00")),
            Iva(id=3, codigo=3, descripcion="IVA No Responsable", porcentaje=Decimal("0.00"), discriminado=True, porcentaje_sobre=Decimal("0.00")),
            Iva(id=4, codigo=4, descripcion="IVA Sujeto Exento", porcentaje=Decimal("0.00"), discriminado=True, porcentaje_sobre=Decimal("0.00")),
            Iva(id=5, codigo=5, descripcion="Consumidor Final", porcentaje=Decimal("0.00"), discriminado=True, porcentaje_sobre=Decimal("0.00")),
            Iva(id=6, codigo=6, descripcion="Responsable Monotributo", porcentaje=Decimal("0.00"), discriminado=True, porcentaje_sobre=Decimal("0.00")),
            Iva(id=8, codigo=8, descripcion="Proveedor del Exterior", porcentaje=Decimal("0.00"), discriminado=True, porcentaje_sobre=Decimal("0.00")),
            Iva(id=9, codigo=9, descripcion="Cliente del Exterior", porcentaje=Decimal("0.00"), discriminado=True, porcentaje_sobre=Decimal("0.00")),
            Iva(id=10, codigo=10, descripcion="IVA Liberado - Ley 19.640", porcentaje=Decimal("0.00"), discriminado=True, porcentaje_sobre=Decimal("0.00")),
            Iva(id=11, codigo=11, descripcion="IVA Responsable Inscripto - Agente de Percepción", porcentaje=Decimal("0.00"), discriminado=True, porcentaje_sobre=Decimal("0.00")),
            Iva(id=13, codigo=13, descripcion="Monotributista Social", porcentaje=Decimal("0.00"), discriminado=True, porcentaje_sobre=Decimal("0.00")),
            Iva(id=15, codigo=15, descripcion="IVA No Alcanzado", porcentaje=Decimal("0.00"), discriminado=True, porcentaje_sobre=Decimal("0.00")),
        ]
        db.add_all(ivas)
        await db.commit()
        print("Seeded IVA")

if __name__ == "__main__":
    asyncio.run(main())
