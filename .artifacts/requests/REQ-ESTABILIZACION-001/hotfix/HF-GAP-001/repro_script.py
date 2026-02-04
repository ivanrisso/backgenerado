import asyncio
import sys
import os
from datetime import date
from sqlalchemy import select, insert, update, text

# Add project root to sys.path
sys.path.append(os.getcwd())

from app.infrastructure.db.engine import SessionLocal
from app.infrastructure.db.orm_models import Comprobante as ComprobanteSQL
from app.infrastructure.db.orm_models import Cliente as ClienteSQL
from app.infrastructure.db.orm_models import TipoComprobante as TipoComprobanteSQL
from app.schemas.comprobante_full import ComprobanteFullCreate, CbteAsoc
from app.schemas.comprobante import ComprobanteCreate
from app.adapters.afip_adapter import AfipAdapter
from app.repositories.comprobante_full_repository import ComprobanteFullUOW
from app.use_cases.comprobante_full_use_case import ComprobanteFullUseCase
from app.domain.entities.comprobante_full import ComprobanteFull

class MockAfipAdapter(AfipAdapter):
    def __init__(self):
        pass

    async def solicitar_cae(self, payload, cabecera):
        # Mock Response
        return {
            "CAE": "12345678901234",
            "CAEFchVto": "20261231"
        }

async def run_verification():
    print("--- Starting Verification for HF-GAP-001 (Partial Imputation) ---")
    
    async with SessionLocal() as db:
        uow = ComprobanteFullUOW(db)
        afip_adapter = MockAfipAdapter()
        use_case = ComprobanteFullUseCase(uow, afip_adapter)
        
        # 1. Setup Data: Ensure Client, TipoComprobante, and Invoice Exists
        
        # Fetch or Create Client
        stmt = select(ClienteSQL).where(ClienteSQL.cuit == "20999999999")
        res = await db.execute(stmt)
        client = res.scalar_one_or_none()
        if not client:
             print("Creating test client...")
             # (Simplified for brevity, assuming existing from previous hotfix or manual insert if needed - repurposing hotfix code logic if needed but let's assume it exists or fail)
             # Actually, let's just insert it to be safe, reusing previous hotfix logic
             stmt = insert(ClienteSQL).values(
                nombre="Test", apellido="Gap001", razon_social="Test Gap 001", cuit="20999999999",
                email="test@gap.com", tipo_doc_id=80, condicion_iva_id=1
             )
             await db.execute(stmt)
             await db.commit()
             # Fetch again
             res = await db.execute(select(ClienteSQL).where(ClienteSQL.cuit == "20999999999"))
             client = res.scalar_one()

        # Fetch or Create TipoComprobante 'FC' (Factura C - Code 11) for Invoice
        stmt = select(TipoComprobanteSQL).where(TipoComprobanteSQL.codigo == "FC")
        res = await db.execute(stmt)
        tipo_fc = res.scalar_one_or_none()
        if not tipo_fc:
             await db.execute(insert(TipoComprobanteSQL).values(codigo="FC", descripcion="Factura C", es_fiscal=True, codigo_arca="011"))
             await db.commit()
             res = await db.execute(select(TipoComprobanteSQL).where(TipoComprobanteSQL.codigo == "FC"))
             tipo_fc = res.scalar_one()

        # Fetch or Create TipoComprobante 'NC' (Nota Credito C - Code 13) for NC
        stmt = select(TipoComprobanteSQL).where(TipoComprobanteSQL.codigo == "NCC")
        res = await db.execute(stmt)
        tipo_nc = res.scalar_one_or_none()
        if not tipo_nc:
             await db.execute(insert(TipoComprobanteSQL).values(codigo="NCC", descripcion="Nota Credito C", es_fiscal=True, codigo_arca="013"))
             await db.commit()
             res = await db.execute(select(TipoComprobanteSQL).where(TipoComprobanteSQL.codigo == "NCC"))
             tipo_nc = res.scalar_one()

        # Cleanup NCs if exist (clean state)
        for nc_num in [999002, 999003]:
             stmt = select(ComprobanteSQL).where(ComprobanteSQL.numero == nc_num)
             res = await db.execute(stmt)
             nc_existing = res.scalar_one_or_none()
             if nc_existing:
                 print(f"Deleting existing NC {nc_num}...")
                 # Also delete imputations if cascade not set?
                 # Assuming cascade or simple delete for test.
                 # Need to delete imputations first manually just in case
                 await db.execute(text(f"DELETE FROM imputacion WHERE comprobante_credito_id = {nc_existing.id}"))
                 await db.delete(nc_existing)
        await db.commit()
        
        # Check if Invoice exists
        invoice_nro = 999001
        stmt = select(ComprobanteSQL).where(ComprobanteSQL.numero == invoice_nro)
        res = await db.execute(stmt)
        invoice = res.scalar_one_or_none()
        
        if invoice:
             print(f"Invoice {invoice_nro} exists. Resetting saldo to 1000...")
             invoice.saldo = 1000.0
             invoice.total = 1000.0
             await db.flush() # Commit later
        else:
             print("Creating Base Invoice with Saldo 1000...")
             stmt = insert(ComprobanteSQL).values(
                cliente_id=client.id, tipo_comprobante_id=tipo_fc.id, concepto_id=1, tipo_doc_id=80, moneda_id=1,
                punto_venta=1, numero=invoice_nro, fecha_emision=date.today(),
                doc_nro=client.cuit, nombre_cliente=client.razon_social, cuit_cliente=client.cuit,
                domicilio_cliente="Street 123", localidad_cliente="City", provincia_cliente="State",
                cotizacion_moneda=1.0, total_neto=1000.0, total_iva=0.0, total_impuestos=0.0, total=1000.0, saldo=1000.0,
                cae="DUMMY", cae_vencimiento=date.today()
             )
             await db.execute(stmt)
        
        await db.commit()
        
        # Reload to be sure
        res = await db.execute(select(ComprobanteSQL).where(ComprobanteSQL.numero == invoice_nro))
        invoice = res.scalar_one()
        print(f"Invoice Ready: ID={invoice.id}, Saldo={invoice.saldo}")

        # --- TEST CASE 1: Partial Imputation ---
        print("\n[TEST 1] Creating NC with Partial Imputation (300)...")
        
        nc_payload = ComprobanteFullCreate(
            cliente_id=client.id,
            tipo_comprobante_id=tipo_nc.id, concepto_id=1, tipo_doc_id=80, moneda_id=1,
            punto_venta=1, numero=999002, fecha_emision=date.today(),
            doc_nro=client.cuit, nombre_cliente=client.razon_social, cuit_cliente=client.cuit,
            domicilio_cliente="Street 123", localidad_cliente="City", provincia_cliente="State", cod_postal_cliente="1234",
            cotizacion_moneda=1.0, total_neto=500.0, total_iva=0.0, total_impuestos=0.0, total=500.0,
            observaciones="Partial Imputation Test",
            detalles=[], impuestos=[],
            cbtes_asociados=[
                CbteAsoc(Tipo=11, PtoVta=1, Nro=invoice_nro, importe_imputar=300.0)
            ]
        )
        
        try:
            nc_result = await use_case.create_comprobante_full(nc_payload)
            print(f"NC Created: ID={nc_result.cabecera.id}, Total={nc_result.cabecera.total}")
            
            # Verify Invoice Saldo
            await db.refresh(invoice)
            print(f"Invoice New Saldo: {invoice.saldo}")
            
            if invoice.saldo == 700.0:
                print("✅ ASSERTION PASSED: Invoice saldo reduced by 300 (1000 -> 700).")
            else:
                print(f"❌ ASSERTION FAILED: Expected 700.0, got {invoice.saldo}")
            
            # Verify NC Saldo
            # NC Total was 500, imputed 300 -> Remaining should be 200?
            if nc_result.cabecera.saldo == 200.0:
                 print("✅ ASSERTION PASSED: NC saldo reduced by 300 (500 -> 200).")
            else:
                 print(f"❌ ASSERTION FAILED: Expected 200.0, got {nc_result.cabecera.saldo}")

        except Exception as e:
            print(f"❌ TEST 1 FAILED: {e}")
            import traceback
            traceback.print_exc()

        # --- TEST CASE 2: Excess Imputation Check ---
        print("\n[TEST 2] Creating NC with Excess Imputation (Factura Saldo Overrun)...")
        # Invoice has 700 left. Try to impute 800.
        
        nc_payload_excess = ComprobanteFullCreate(
            cliente_id=client.id,
            tipo_comprobante_id=tipo_nc.id, concepto_id=1, tipo_doc_id=80, moneda_id=1,
            punto_venta=1, numero=999003, fecha_emision=date.today(),
            doc_nro=client.cuit, nombre_cliente=client.razon_social, cuit_cliente=client.cuit,
            domicilio_cliente="Street 123", localidad_cliente="City", provincia_cliente="State", cod_postal_cliente="1234",
            cotizacion_moneda=1.0, total_neto=500.0, total_iva=0.0, total_impuestos=0.0, total=500.0,
            observaciones="Excess Test",
            detalles=[], impuestos=[],
            cbtes_asociados=[
                CbteAsoc(Tipo=11, PtoVta=1, Nro=invoice_nro, importe_imputar=800.0)
            ]
        )
        
        try:
            await use_case.create_comprobante_full(nc_payload_excess)
            print("❌ ASSERTION FAILED: Expected 400 Error, got Success")
        except Exception as e:
            if "excede el saldo de la factura" in str(e):
                 print("✅ ASSERTION PASSED: Caught expected validation error (Invoice Balance).")
            else:
                 print(f"⚠️ Unexpected Error: {e}")

        # Cleanup
        # (Optional, SQLite is local)

if __name__ == "__main__":
    asyncio.run(run_verification())
