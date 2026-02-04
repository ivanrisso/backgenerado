import asyncio
import sys
import os
from datetime import date
from sqlalchemy import insert, select, text

# Add project root to sys.path
sys.path.append(os.getcwd())

from app.infrastructure.db.engine import SessionLocal
from app.infrastructure.db.orm_models import Cliente as ClienteSQL
from app.infrastructure.db.orm_models import TipoComprobante as TipoComprobanteSQL
from app.repositories.cliente_repository import ClienteRepositoryImpl
from app.repositories.comprobante_repository import ComprobanteRepositoryImpl
from app.repositories.tipocomprobante_repository import TipoComprobanteRepositoryImpl
from app.repositories.imputacion_repository import ImputacionRepositoryImpl
from app.repositories.cuentacorriente_repository import CuentaCorrienteRepositoryImpl
from app.services.recibo_service import ReciboService
from app.schemas.recibo import ReciboCreate
from app.domain.entities.cliente import Cliente
from app.domain.exceptions.cliente import ClienteNoEncontrado

async def run_verification():
    print("--- Starting Verification for HOTFIX-BE-002 ---")
    
    async with SessionLocal() as db:
        # 1. Setup Repositories and Service
        cliente_repo = ClienteRepositoryImpl(db)
        comp_repo = ComprobanteRepositoryImpl(db)
        tipo_repo = TipoComprobanteRepositoryImpl(db)
        imp_repo = ImputacionRepositoryImpl(db)
        cc_repo = CuentaCorrienteRepositoryImpl(db)
        
        service = ReciboService(comp_repo, tipo_repo, imp_repo, cc_repo, cliente_repo)
        
        # 2. Setup Test Data (Cliente)
        test_cuit = "20999999999"
        stmt = select(ClienteSQL).where(ClienteSQL.cuit == test_cuit)
        result = await db.execute(stmt)
        target_client_sql = result.scalar_one_or_none()
        
        target_id = None
        target_razon_social = "Test Hotfix BE-002 S.A."
        
        if not target_client_sql:
            print("Creating test client manually...")
            # Using correct columns for Cliente based on orm_models.py
            stmt = insert(ClienteSQL).values(
                nombre="Test",
                apellido="Hotfix",
                razon_social=target_razon_social,
                cuit=test_cuit,
                email="test@hotfix.com",
                tipo_doc_id=80, # CUIT
                condicion_iva_id=1
            )
            await db.execute(stmt)
            await db.commit()
            
            stmt = select(ClienteSQL).where(ClienteSQL.cuit == test_cuit)
            result = await db.execute(stmt)
            target_client_sql = result.scalar_one()
            target_id = target_client_sql.id
            print(f"Client created: ID={target_id}")
        else:
            target_id = target_client_sql.id
            target_razon_social = target_client_sql.razon_social
            target_razon_social = target_client_sql.razon_social if target_client_sql.razon_social else f"{target_client_sql.nombre} {target_client_sql.apellido}"
            print(f"Using existing test client: ID={target_id}")

        # 3. Setup Test Data (TipoComprobante - RC)
        stmt = select(TipoComprobanteSQL).where(TipoComprobanteSQL.codigo.in_(["RC", "REC"]))
        result = await db.execute(stmt)
        tipo_recibo_sql = result.scalar_one_or_none()
        
        if not tipo_recibo_sql:
            print("Creating TipoComprobante 'RC' manually...")
            # Correct columns
            stmt = insert(TipoComprobanteSQL).values(
                codigo="RC",
                descripcion="Recibo X",
                es_fiscal=False,
                codigo_arca="004" 
            )
            await db.execute(stmt)
            await db.commit()
            print("TipoComprobante 'RC' created.")
        else:
             print(f"Using existing TipoComprobante: {tipo_recibo_sql.codigo}")

        # 4. Test Case 1: Create Recibo with Valid Client
        print("\n[TEST 1] Creating Recibo for valid client...")
        recibo_data = ReciboCreate(
            cliente_id=target_id,
            punto_venta=1,
            fecha_emision=date.today(),
            total=100.0,
            observaciones="Test Hotfix BE-002",
            imputaciones=[]
        )
        
        try:
            recibo_response = await service.create_recibo(recibo_data)
            print(f"Recibo created ID: {recibo_response.id}")
            
            # Fetch from DB to verify persistence details (as response schema is partial)
            recibo_db = await comp_repo.get_by_id(recibo_response.id)
            
            print(f"Client Name in DB Recibo: '{recibo_db.nombre_cliente}'")
            print(f"Client CUIT in DB Recibo: '{recibo_db.cuit_cliente}'")
            print(f"Doc Nro in DB Recibo: '{recibo_db.doc_nro}'")
            
            # ASSERTIONS
            if target_razon_social in recibo_db.nombre_cliente or recibo_db.nombre_cliente in target_razon_social:
                print("✅ ASSERTION PASSED: nombre_cliente matches client data.")
            else:
                print(f"❌ ASSERTION FAILED: Expected '{target_razon_social}', got '{recibo_db.nombre_cliente}'")
                
            if recibo_db.cuit_cliente == test_cuit:
                 print("✅ ASSERTION PASSED: cuit_cliente matches client data.")
            else:
                 print(f"❌ ASSERTION FAILED: Expected '{test_cuit}', got '{recibo_db.cuit_cliente}'")

            if recibo_db.doc_nro != "00000000":
                 print(f"✅ ASSERTION PASSED: doc_nro is not placeholder ({recibo_db.doc_nro}).")
            else:
                 print("❌ ASSERTION FAILED: doc_nro is still default placeholder.")

        except Exception as e:
            print(f"❌ TEST 1 FAILED with error: {e}")
            import traceback
            traceback.print_exc()

        # 5. Test Case 2: Create Recibo with Invalid Client
        print("\n[TEST 2] Creating Recibo for NON-EXISTENT client (ID=999999)...")
        recibo_data_inv = ReciboCreate(
            cliente_id=999999,
            punto_venta=1,
            fecha_emision=date.today(),
            total=50.0,
            observaciones="Should Fail",
            imputaciones=[]
        )
        
        try:
            await service.create_recibo(recibo_data_inv)
            print("❌ ASSERTION FAILED: Expected ClienteNoEncontrado, but Recibo was created.")
        except ClienteNoEncontrado:
            print("✅ ASSERTION PASSED: Caught Expected ClienteNoEncontrado exception.")
        except Exception as e:
            print(f"❌ TEST 2 FAILED with unexpected error: {type(e).__name__}: {e}")

if __name__ == "__main__":
    asyncio.run(run_verification())
