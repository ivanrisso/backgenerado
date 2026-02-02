import asyncio
from sqlalchemy import text
from app.infrastructure.db.engine import SessionLocal

async def fix_hard():
    async with SessionLocal() as session:
        print("Executing Hard Enum Fix...")
        
        # Operations for TipoImpuesto
        
        # Categoria
        await session.execute(text("ALTER TABLE tipoimpuesto MODIFY categoria VARCHAR(50)"))
        await session.execute(text("UPDATE tipoimpuesto SET categoria = UPPER(categoria)"))
        await session.execute(text("ALTER TABLE tipoimpuesto MODIFY categoria ENUM('IMPUESTO_DIRECTO','PERCEPCION','RETENCION','TASA','OTRO') NOT NULL DEFAULT 'IMPUESTO_DIRECTO'"))
        
        # Tipo Aplicacion
        await session.execute(text("ALTER TABLE tipoimpuesto MODIFY tipo_aplicacion VARCHAR(50)"))
        await session.execute(text("UPDATE tipoimpuesto SET tipo_aplicacion = UPPER(tipo_aplicacion)"))
        await session.execute(text("ALTER TABLE tipoimpuesto MODIFY tipo_aplicacion ENUM('SUMA','DESCUENTO','NEUTRO') NOT NULL"))
        
        # Base Calculo
        await session.execute(text("ALTER TABLE tipoimpuesto MODIFY base_calculo VARCHAR(50)"))
        await session.execute(text("UPDATE tipoimpuesto SET base_calculo = UPPER(base_calculo)"))
        await session.execute(text("ALTER TABLE tipoimpuesto MODIFY base_calculo ENUM('SUBTOTAL','TOTAL','NETO_GRAVADO','OTROS') NOT NULL"))
        
        # Ambito (TipoImpuesto)
        await session.execute(text("ALTER TABLE tipoimpuesto MODIFY ambito VARCHAR(50)"))
        await session.execute(text("UPDATE tipoimpuesto SET ambito = UPPER(ambito)"))
        await session.execute(text("ALTER TABLE tipoimpuesto MODIFY ambito ENUM('NACIONAL','PROVINCIAL','MUNICIPAL') NOT NULL DEFAULT 'NACIONAL'"))
        
        # Tipo Uso
        await session.execute(text("ALTER TABLE tipoimpuesto MODIFY tipo_uso VARCHAR(50)"))
        await session.execute(text("UPDATE tipoimpuesto SET tipo_uso = UPPER(tipo_uso)"))
        await session.execute(text("ALTER TABLE tipoimpuesto MODIFY tipo_uso ENUM('VENTAS','COMPRAS','OTRO','RETENCION_PAGO_PROVEEDOR','RETENCION_PAGO_CLIENTE') NOT NULL DEFAULT 'VENTAS'"))
        
        # Metodo Calculo
        await session.execute(text("ALTER TABLE tipoimpuesto MODIFY metodo_calculo VARCHAR(50)"))
        await session.execute(text("UPDATE tipoimpuesto SET metodo_calculo = UPPER(metodo_calculo)"))
        await session.execute(text("ALTER TABLE tipoimpuesto MODIFY metodo_calculo ENUM('PORCENTAJE','FIJO','PORCENTAJE_SOBRE_PRECIO','GRUPO') NOT NULL DEFAULT 'PORCENTAJE'"))
        
        # Ambito Uso
        await session.execute(text("ALTER TABLE tipoimpuesto MODIFY ambito_uso VARCHAR(50)"))
        await session.execute(text("UPDATE tipoimpuesto SET ambito_uso = UPPER(ambito_uso)"))
        await session.execute(text("ALTER TABLE tipoimpuesto MODIFY ambito_uso ENUM('BIENES','SERVICIOS','AMBOS') NOT NULL DEFAULT 'AMBOS'"))
        
        # Operations for CondicionTributaria
        
        # Ambito
        await session.execute(text("ALTER TABLE condiciontributaria MODIFY ambito VARCHAR(50)"))
        await session.execute(text("UPDATE condiciontributaria SET ambito = UPPER(ambito)"))
        await session.execute(text("ALTER TABLE condiciontributaria MODIFY ambito ENUM('NACIONAL','PROVINCIAL','MUNICIPAL') NOT NULL DEFAULT 'NACIONAL'"))
        
        await session.commit()
        print("Hard Fix Complete.")

if __name__ == "__main__":
    asyncio.run(fix_hard())
