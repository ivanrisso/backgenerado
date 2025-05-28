# app/domain/exceptions/tipocomprobante.py

class TipoComprobanteNoEncontrado(Exception):
    """Se lanza cuando no se encuentra un tipocomprobante con el ID proporcionado."""
    def __init__(self, tipocomprobante_id: int):
        self.tipocomprobante_id = tipocomprobante_id
        self.message = f"TipoComprobante con ID {tipocomprobante_id} no encontrado"
        super().__init__(self.message)


class TipoComprobanteDuplicado(Exception):
    """Se lanza cuando se intenta crear un tipocomprobante con un valor único duplicado (ej. email o CUIT)."""
    def __init__(self, campo: str, valor: str):
        self.campo = campo
        self.valor = valor
        self.message = f"Ya existe un tipocomprobante con {campo} = {valor}"
        super().__init__(self.message)


class TipoComprobanteInvalido(Exception):
    """Se lanza cuando los datos del tipocomprobante no cumplen alguna regla de negocio del dominio."""
    def __init__(self, razon: str):
        self.message = f"TipoComprobante inválido: {razon}"
        super().__init__(self.message)

