
from sqlalchemy import create_engine, text
import json
import os

# Configuración de base de datos (ajustar según entorno local)
DATABASE_URL = "mysql+pymysql://app:app@localhost:3306/facturacion"

def run_migration():
    print("Iniciando migración de Vouchers...")
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        # Verificar si la columna ya existe
        result = conn.execute(text("SHOW COLUMNS FROM comprobantedetalle LIKE 'datos_extra'"))
        if result.fetchone():
            print("La columna 'datos_extra' ya existe en 'comprobantedetalle'.")
        else:
            print("Agregando columna 'datos_extra' a tabla 'comprobantedetalle'...")
            try:
                # MySQL 5.7+ soporta JSON. MariaDB 10.2+ soporta JSON (como alias de LONGTEXT con chequeo).
                # Asumimos soporte JSON o usamos TEXT si falla.
                conn.execute(text("ALTER TABLE comprobantedetalle ADD COLUMN datos_extra JSON NULL"))
                print("Columna agregada exitosamente.")
            except Exception as e:
                print(f"Error al agregar columna JSON: {e}")
                print("Intentando agregar como TEXT para compatibilidad...")
                conn.execute(text("ALTER TABLE comprobantedetalle ADD COLUMN datos_extra TEXT NULL"))
                print("Columna agregada como TEXT.")
        
    print("Migración completada.")

if __name__ == "__main__":
    run_migration()
