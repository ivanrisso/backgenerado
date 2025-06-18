# app/domain/entities/comprobante_full.py

from typing import List
from datetime import date
from app.domain.entities.comprobante import Comprobante
from app.domain.entities.comprobantedetalle import ComprobanteDetalle
from app.domain.entities.comprobanteimpuesto import ComprobanteImpuesto

class ComprobanteFull:
    def __init__(
        self,
        cabecera: Comprobante,
        detalles: List[ComprobanteDetalle],
        impuestos: List[ComprobanteImpuesto],
    ):
        self.cabecera = cabecera
        self.detalles = detalles
        self.impuestos = impuestos
