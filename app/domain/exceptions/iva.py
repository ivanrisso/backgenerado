# app/domain/exceptions/iva.py

class IvaNoEncontrado(Exception):
    """Se lanza cuando no se encuentra un iva con el ID proporcionado."""
    def __init__(self, iva_id: int):
        self.iva_id = iva_id
        self.message = f"Iva con ID {iva_id} no encontrado"
        super().__init__(self.message)


class IvaDuplicado(Exception):
    """Se lanza cuando se intenta crear un iva con un valor único duplicado (ej. email o CUIT)."""
    def __init__(self, campo: str, valor: str):
        self.campo = campo
        self.valor = valor
        self.message = f"Ya existe un iva con {campo} = {valor}"
        super().__init__(self.message)


class IvaInvalido(Exception):
    """Se lanza cuando los datos del iva no cumplen alguna regla de negocio del dominio."""
    def __init__(self, razon: str):
        self.message = f"Iva inválido: {razon}"
        super().__init__(self.message)

