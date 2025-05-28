# app/domain/exceptions/pais.py

class PaisNoEncontrado(Exception):
    """Se lanza cuando no se encuentra un pais con el ID proporcionado."""
    def __init__(self, pais_id: int):
        self.pais_id = pais_id
        self.message = f"Pais con ID {pais_id} no encontrado"
        super().__init__(self.message)


class PaisDuplicado(Exception):
    """Se lanza cuando se intenta crear un pais con un valor único duplicado (ej. email o CUIT)."""
    def __init__(self, campo: str, valor: str):
        self.campo = campo
        self.valor = valor
        self.message = f"Ya existe un pais con {campo} = {valor}"
        super().__init__(self.message)


class PaisInvalido(Exception):
    """Se lanza cuando los datos del pais no cumplen alguna regla de negocio del dominio."""
    def __init__(self, razon: str):
        self.message = f"Pais inválido: {razon}"
        super().__init__(self.message)

