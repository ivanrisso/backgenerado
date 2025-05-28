# app/domain/exceptions/comprobante.py

class ComprobanteNoEncontrado(Exception):
    """Se lanza cuando no se encuentra un comprobante con el ID proporcionado."""
    def __init__(self, comprobante_id: int):
        self.comprobante_id = comprobante_id
        self.message = f"Comprobante con ID {comprobante_id} no encontrado"
        super().__init__(self.message)


class ComprobanteDuplicado(Exception):
    """Se lanza cuando se intenta crear un comprobante con un valor único duplicado (ej. email o CUIT)."""
    def __init__(self, campo: str, valor: str):
        self.campo = campo
        self.valor = valor
        self.message = f"Ya existe un comprobante con {campo} = {valor}"
        super().__init__(self.message)


class ComprobanteInvalido(Exception):
    """Se lanza cuando los datos del comprobante no cumplen alguna regla de negocio del dominio."""
    def __init__(self, razon: str):
        self.message = f"Comprobante inválido: {razon}"
        super().__init__(self.message)

