# app/domain/exceptions/auditoriacomprobante.py

class AuditoriaComprobanteNoEncontrado(Exception):
    """Se lanza cuando no se encuentra un auditoriacomprobante con el ID proporcionado."""
    def __init__(self, auditoriacomprobante_id: int):
        self.auditoriacomprobante_id = auditoriacomprobante_id
        self.message = f"AuditoriaComprobante con ID {auditoriacomprobante_id} no encontrado"
        super().__init__(self.message)


class AuditoriaComprobanteDuplicado(Exception):
    """Se lanza cuando se intenta crear un auditoriacomprobante con un valor único duplicado (ej. email o CUIT)."""
    def __init__(self, campo: str, valor: str):
        self.campo = campo
        self.valor = valor
        self.message = f"Ya existe un auditoriacomprobante con {campo} = {valor}"
        super().__init__(self.message)


class AuditoriaComprobanteInvalido(Exception):
    """Se lanza cuando los datos del auditoriacomprobante no cumplen alguna regla de negocio del dominio."""
    def __init__(self, razon: str):
        self.message = f"AuditoriaComprobante inválido: {razon}"
        super().__init__(self.message)

