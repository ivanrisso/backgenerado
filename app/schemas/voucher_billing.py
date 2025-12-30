from pydantic import BaseModel

class VoucherBillingRequest(BaseModel):
    voucher_id: str
    cliente_id: int
    punto_venta: int
    tipo_comprobante_id: int
    concepto_id: int
