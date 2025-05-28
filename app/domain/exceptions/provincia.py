# app/domain/exceptions/provincia.py
class ProvinciaNoEncontrado(Exception):
    """Se lanza cuando no se encuentra un provincia con el ID proporcionado."""
    def __init__(self, provincia_id: int):
        self.provincia_id = provincia_id
        self.message = f"Provincia con ID {provincia_id} no encontrado"
        super().__init__(self.message)


class ProvinciaDuplicado(Exception):
    """Se lanza cuando se intenta crear un provincia con un valor único duplicado (ej. email o CUIT)."""
    def __init__(self, campo: str, valor: str):
        self.campo = campo
        self.valor = valor
        self.message = f"Ya existe un provincia con {campo} = {valor}"
        super().__init__(self.message)


class ProvinciaInvalido(Exception):
    """Se lanza cuando los datos del provincia no cumplen alguna regla de negocio del dominio."""
    def __init__(self, razon: str):
        self.message = f"Provincia inválido: {razon}"
        super().__init__(self.message)

