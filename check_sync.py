
import asyncio
from app.infrastructure.db.engine import SessionLocal
from app.infrastructure.db.orm_models import Comprobante
from sqlalchemy import select, func
from app.core.afip_client import get_afip_client

async def check_sync():
    # 1. Check DB
    async with SessionLocal() as session:
        result = await session.execute(select(func.max(Comprobante.numero)).where(Comprobante.tipo_comprobante_id == 1))
        max_db = result.scalar() or 0
        print(f"Ultimo Comprobante en DB (Tipo A?): {max_db}")

    # 2. Check AFIP
    try:
        client = get_afip_client()
        # Need correct params: PtoVta (5?), Tipo (01 for A)
        # Assuming defaults from collection
        token, sign = client.wsaa_client.get_token_and_sign()
        
        # Manually call FECompUltimoAutorizado logic or import WSFEClient
        # Trying to reuse existing logic if possible, or raw zeep
        from zeep import Client
        wsfe = Client(client.wsdl)
        auth = {"Token": token, "Sign": sign, "Cuit": client.cuit}
        
        resp = wsfe.service.FECompUltimoAutorizado(Auth=auth, PtoVta=5, CbteTipo=1) # 1 is Code 01? No, Code 1 is A.
        # Wait, FECompUltimoAutorizado takes Int. But Types are "01", "06".
        # Usually it accepts integer 1.
        
        print(f"Ultimo Comprobante en AFIP (PtoVta 5, Oba A): {resp.CbteNro}")
        
    except Exception as e:
        print(f"Error checking AFIP: {e}")

if __name__ == "__main__":
    asyncio.run(check_sync())
