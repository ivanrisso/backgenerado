
import asyncio
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.future import select
from app.infrastructure.db.orm_models import Articulo, TipoImpuesto, TipoArticuloEnum
from app.infrastructure.db.engine import SessionLocal

async def seed_articulos():
    async with SessionLocal() as db:
        try:
            # Get taxes (IVA 21% and 10.5%)
            result_21 = await db.execute(select(TipoImpuesto).filter(TipoImpuesto.nombre.like('%21%')))
            iva21 = result_21.scalars().first()
            
            result_105 = await db.execute(select(TipoImpuesto).filter(TipoImpuesto.nombre.like('%10.5%')))
            iva105 = result_105.scalars().first()
            
            if not iva21:
                 print("IVA 21% non found")
            
            articulos_data = [
                {
                    "codigo": "SERV-001",
                    "nombre": "Servicio de Traslado Aeropuerto",
                    "descripcion": "Traslado ejecutivo desde Ezeiza a CABA",
                    "precio_venta": 45000.0,
                    "precio_costo": 25000.0,
                    "tipo": TipoArticuloEnum.SERVICIO,
                    "impuesto_venta_id": iva21.id if iva21 else None,
                    "impuesto_compra_id": iva21.id if iva21 else None,
                },
                {
                    "codigo": "SERV-002",
                    "nombre": "City Tour Buenos Aires (Medio Día)",
                    "descripcion": "Recorrido por los puntos históricos de la ciudad",
                    "precio_venta": 15000.0,
                    "precio_costo": 8000.0,
                    "tipo": TipoArticuloEnum.SERVICIO,
                    "impuesto_venta_id": iva21.id if iva21 else None,
                    "impuesto_compra_id": iva21.id if iva21 else None,
                },
                {
                    "codigo": "SERV-003",
                    "nombre": "Hospedaje Noche Extra",
                    "descripcion": "Noche adicional en hotel categoría superior",
                    "precio_venta": 85000.0,
                    "precio_costo": 60000.0,
                    "tipo": TipoArticuloEnum.SERVICIO,
                    "impuesto_venta_id": iva105.id if iva105 else None,
                    "impuesto_compra_id": iva105.id if iva105 else None,
                }
            ]
            
            for data in articulos_data:
                result = await db.execute(select(Articulo).filter(Articulo.codigo == data["codigo"]))
                existing = result.scalars().first()
                if not existing:
                    articulo = Articulo(**data)
                    db.add(articulo)
                    print(f"Added articulo: {data['nombre']}")
                else:
                    print(f"Articulo already exists: {data['nombre']}")
            
            await db.commit()
            print("Seeding completed successfully!")
        except Exception as e:
            await db.rollback()
            print(f"Error during seeding: {e}")

if __name__ == "__main__":
    asyncio.run(seed_articulos())
