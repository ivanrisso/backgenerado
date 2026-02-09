from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class ImputacionCreate(BaseModel):
    comprobante_deuda_id: int
    importe: float

class ReciboCreate(BaseModel):
    cliente_id: int
    fecha_emision: date
    punto_venta: int
    total: float
    observaciones: Optional[str] = None
    imputaciones: List[ImputacionCreate] = []

class ReciboResponse(BaseModel):
    id: int
    numero: int
    fecha_emision: date
    total: float
    saldo: float
    cliente_id: int
    nombre_cliente: Optional[str] = None
    observaciones: Optional[str]
    # Podríamos agregar detalles de imputaciones aquí si fuera necesario
    
    class Config:
        from_attributes = True
