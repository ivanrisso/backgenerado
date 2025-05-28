# app/domain/exceptions/comprobanteimpuesto.py

class ComprobanteImpuestoNoEncontrado(Exception):
    """Se lanza cuando no se encuentra un comprobanteimpuesto con el ID proporcionado."""
    def __init__(self, comprobanteimpuesto_id: int):
        self.comprobanteimpuesto_id = comprobanteimpuesto_id
        self.message = f"ComprobanteImpuesto con ID {comprobanteimpuesto_id} no encontrado"
        super().__init__(self.message)


class ComprobanteImpuestoDuplicado(Exception):
    """Se lanza cuando se intenta crear un comprobanteimpuesto con un valor único duplicado (ej. email o CUIT)."""
    def __init__(self, campo: str, valor: str):
        self.campo = campo
        self.valor = valor
        self.message = f"Ya existe un comprobanteimpuesto con {campo} = {valor}"
        super().__init__(self.message)


class ComprobanteImpuestoInvalido(Exception):
    """Se lanza cuando los datos del comprobanteimpuesto no cumplen alguna regla de negocio del dominio."""
    def __init__(self, razon: str):
        self.message = f"ComprobanteImpuesto inválido: {razon}"
        super().__init__(self.message)

