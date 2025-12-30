from typing import Optional
from app.domain.entities.voucher import Voucher
from app.domain.repository.voucher_repository_interface import VoucherRepositoryInterface
# import pyodbc (Would be used in real scenario)

class ExternalVoucherRepository(VoucherRepositoryInterface):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    async def get_by_id(self, voucher_id: str) -> Optional[Voucher]:
        """
        Simulates fetching a voucher from an external SQL Server.
        In a real implementation, this would use pyodbc or sqlalchemy to query the external DB.
        """
        print(f"DEBUG: Connecting to External DB at {self.connection_string} for Voucher {voucher_id}")
        
        # REAL IMPLEMENTATION EXAMPLE:
        # query = "SELECT CupIte, CupNroVou, CupImporte, CupVou1, CupCliente FROM CUPONES WHERE CupNroVou = ?"
        # row = cursor.execute(query, voucher_id).fetchone()
        
        # MOCK DATA for testing
        if voucher_id == "VOU-001":
            return Voucher(
                id="1001", # CupIte
                nro_voucher="VOU-001", # CupNroVou
                monto_neto_ope=1500.00, # CupNetoOpe
                monto_neto_gsa=0.00,    # CupNetoGSA
                monto_impuestos=0.00,
                descripcion="Alquiler Auto Compacto - 3 Días",
                ref_cliente="CLI-123", # CupCliente
                sistema_origen="SQL_SERVER"
            )
        elif voucher_id == "VOU-002":
             return Voucher(
                id="1002",
                nro_voucher="VOU-002",
                monto_neto_ope=25000.00,
                monto_neto_gsa=5000.00,
                monto_impuestos=120.00, # CupImpoTax
                descripcion="Alquiler Camioneta - 1 Semana",
                ref_cliente="CLI-456",
                sistema_origen="SQL_SERVER"
            )
            
        return None
