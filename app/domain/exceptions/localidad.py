# app/domain/exceptions/localidad.py

class LocalidadNoEncontrado(Exception):
    """Se lanza cuando no se encuentra un localidad con el ID proporcionado."""
    def __init__(self, localidad_id: int):
        self.localidad_id = localidad_id
        self.message = f"Localidad con ID {localidad_id} no encontrado"
        super().__init__(self.message)


class LocalidadDuplicado(Exception):
    """Se lanza cuando se intenta crear un localidad con un valor único duplicado (ej. email o CUIT)."""
    def __init__(self, campo: str, valor: str):
        self.campo = campo
        self.valor = valor
        self.message = f"Ya existe un localidad con {campo} = {valor}"
        super().__init__(self.message)


class LocalidadInvalido(Exception):
    """Se lanza cuando los datos del localidad no cumplen alguna regla de negocio del dominio."""
    def __init__(self, razon: str):
        self.message = f"Localidad inválido: {razon}"
        super().__init__(self.message)

