# app/domain/exceptions/comprobantedetalle.py

class ComprobanteDetalleNoEncontrado(Exception):
    """Se lanza cuando no se encuentra un comprobantedetalle con el ID proporcionado."""
    def __init__(self, comprobantedetalle_id: int):
        self.comprobantedetalle_id = comprobantedetalle_id
        self.message = f"ComprobanteDetalle con ID {comprobantedetalle_id} no encontrado"
        super().__init__(self.message)


class ComprobanteDetalleDuplicado(Exception):
    """Se lanza cuando se intenta crear un comprobantedetalle con un valor único duplicado (ej. email o CUIT)."""
    def __init__(self, campo: str, valor: str):
        self.campo = campo
        self.valor = valor
        self.message = f"Ya existe un comprobantedetalle con {campo} = {valor}"
        super().__init__(self.message)


class ComprobanteDetalleInvalido(Exception):
    """Se lanza cuando los datos del comprobantedetalle no cumplen alguna regla de negocio del dominio."""
    def __init__(self, razon: str):
        self.message = f"ComprobanteDetalle inválido: {razon}"
        super().__init__(self.message)

