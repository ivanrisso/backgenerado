
import sys
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

sys.path.append('/home/irisso/proyectos/facturacion')

DATABASE_URL = "mysql+asyncmy://app:app@localhost:3306/facturacion"
engine = create_async_engine(DATABASE_URL, echo=False)

async def migrate():
    async with engine.begin() as conn:
        print("Checking if 'orden' column exists...")
        try:
            # Check if column exists
            await conn.execute(text("SELECT orden FROM menuitem LIMIT 1"))
            print("Column 'orden' already exists.")
        except Exception:
            print("Column 'orden' does not exist. Adding it...")
            await conn.execute(text("ALTER TABLE menuitem ADD COLUMN orden INT DEFAULT 0"))
            print("Column added.")
        
        print("Updating initial order values...")
        # Define initial order
        updates = [
            (29, 0),   # Dashboard
            (28, 10),  # Cuenta Corriente
            (22, 20),  # Comprobantes (Group)
            (26, 21),  # Listado (Comprobantes Child)
            (27, 22),  # Facturas (Comprobantes Child)
            (31, 30),  # Tesorería (Group)
            (32, 31),  # Recibos (Tesorería Child)
            (33, 40),  # Puntos de Venta
            (16, 50),  # Clientes
            (23, 51),  # Domicilios
            (24, 52),  # Teléfonos
            (17, 60),  # Países
            (18, 61),  # Provincias
            (19, 62),  # Localidades
            (20, 63),  # Tipos Domicilio
            (21, 64),  # Tipos Teléfono
            (7, 70),   # Operadores
            (8, 71),   # Tipos Comprobante
            (9, 72),   # Conceptos
            (10, 73),  # Monedas
            (11, 74),  # IVAs
            (12, 75),  # Tipos Impuesto
            (4, 90),   # Seguridad (Group)
            (13, 91),  # Usuarios
            (14, 92),  # Roles
            (15, 93),  # Menús
            (3, 100),  # Configuración (Group)
        ]
        
        for mid, orden in updates:
            await conn.execute(
                text("UPDATE menuitem SET orden = :o WHERE id = :id"),
                {"o": orden, "id": mid}
            )
            
        print("Order values updated.")

if __name__ == "__main__":
    asyncio.run(migrate())
