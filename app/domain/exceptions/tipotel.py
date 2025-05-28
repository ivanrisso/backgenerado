# app/domain/exceptions/tipotel.py

class TipoTelNoEncontrado(Exception):
    """Se lanza cuando no se encuentra un tipotel con el ID proporcionado."""
    def __init__(self, tipotel_id: int):
        self.tipotel_id = tipotel_id
        self.message = f"TipoTel con ID {tipotel_id} no encontrado"
        super().__init__(self.message)


class TipoTelDuplicado(Exception):
    """Se lanza cuando se intenta crear un tipotel con un valor único duplicado (ej. email o CUIT)."""
    def __init__(self, campo: str, valor: str):
        self.campo = campo
        self.valor = valor
        self.message = f"Ya existe un tipotel con {campo} = {valor}"
        super().__init__(self.message)


class TipoTelInvalido(Exception):
    """Se lanza cuando los datos del tipotel no cumplen alguna regla de negocio del dominio."""
    def __init__(self, razon: str):
        self.message = f"TipoTel inválido: {razon}"
        super().__init__(self.message)

