# app/domain/exceptions/moneda.py

class MonedaNoEncontrado(Exception):
    """Se lanza cuando no se encuentra un moneda con el ID proporcionado."""
    def __init__(self, moneda_id: int):
        self.moneda_id = moneda_id
        self.message = f"Moneda con ID {moneda_id} no encontrado"
        super().__init__(self.message)


class MonedaDuplicado(Exception):
    """Se lanza cuando se intenta crear un moneda con un valor único duplicado (ej. email o CUIT)."""
    def __init__(self, campo: str, valor: str):
        self.campo = campo
        self.valor = valor
        self.message = f"Ya existe un moneda con {campo} = {valor}"
        super().__init__(self.message)


class MonedaInvalido(Exception):
    """Se lanza cuando los datos del moneda no cumplen alguna regla de negocio del dominio."""
    def __init__(self, razon: str):
        self.message = f"Moneda inválido: {razon}"
        super().__init__(self.message)

