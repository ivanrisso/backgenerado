import asyncio
from sqlalchemy import text
from app.infrastructure.db.engine import SessionLocal

async def fix_enums():
    async with SessionLocal() as session:
        print("Fixing Enum values in DB...")
        
        # TipoImpuesto Enums
        # categoria: impuesto_directo -> IMPUESTO_DIRECTO
        # tipo_aplicacion, base_calculo, ambito, tipo_uso, metodo_calculo, ambito_uso
        
        # We'll run raw SQL updates for known lowercase values to uppercase
        # MySQL/MariaDB unquoted identifiers are case-insensitive usually, but values are case sensitive.
        
        queries = [
            "UPDATE tipoimpuesto SET categoria = UPPER(categoria)",
            "UPDATE tipoimpuesto SET tipo_aplicacion = UPPER(tipo_aplicacion)",
            "UPDATE tipoimpuesto SET base_calculo = UPPER(base_calculo)",
            "UPDATE tipoimpuesto SET ambito = UPPER(ambito)",
            "UPDATE tipoimpuesto SET tipo_uso = UPPER(tipo_uso)",
            "UPDATE tipoimpuesto SET metodo_calculo = UPPER(metodo_calculo)",
            "UPDATE tipoimpuesto SET ambito_uso = UPPER(ambito_uso)",
            
            "UPDATE condiciontributaria SET ambito = UPPER(ambito)"
        ]
        
        for q in queries:
            print(f"Executing: {q}")
            await session.execute(text(q))
            
        await session.commit()
        print("Enums fixed.")

if __name__ == "__main__":
    asyncio.run(fix_enums())
