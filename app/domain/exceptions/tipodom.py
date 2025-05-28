# app/domain/exceptions/tipodom.py

class TipoDomNoEncontrado(Exception):
    """Se lanza cuando no se encuentra un tipodom con el ID proporcionado."""
    def __init__(self, tipodom_id: int):
        self.tipodom_id = tipodom_id
        self.message = f"TipoDom con ID {tipodom_id} no encontrado"
        super().__init__(self.message)


class TipoDomDuplicado(Exception):
    """Se lanza cuando se intenta crear un tipodom con un valor único duplicado (ej. email o CUIT)."""
    def __init__(self, campo: str, valor: str):
        self.campo = campo
        self.valor = valor
        self.message = f"Ya existe un tipodom con {campo} = {valor}"
        super().__init__(self.message)


class TipoDomInvalido(Exception):
    """Se lanza cuando los datos del tipodom no cumplen alguna regla de negocio del dominio."""
    def __init__(self, razon: str):
        self.message = f"TipoDom inválido: {razon}"
        super().__init__(self.message)

