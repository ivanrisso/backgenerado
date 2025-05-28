# app/domain/exceptions/domicilio.py

class DomicilioNoEncontrado(Exception):
    """Se lanza cuando no se encuentra un domicilio con el ID proporcionado."""
    def __init__(self, domicilio_id: int):
        self.domicilio_id = domicilio_id
        self.message = f"Domicilio con ID {domicilio_id} no encontrado"
        super().__init__(self.message)


class DomicilioDuplicado(Exception):
    """Se lanza cuando se intenta crear un domicilio con un valor único duplicado (ej. email o CUIT)."""
    def __init__(self, campo: str, valor: str):
        self.campo = campo
        self.valor = valor
        self.message = f"Ya existe un domicilio con {campo} = {valor}"
        super().__init__(self.message)


class DomicilioInvalido(Exception):
    """Se lanza cuando los datos del domicilio no cumplen alguna regla de negocio del dominio."""
    def __init__(self, razon: str):
        self.message = f"Domicilio inválido: {razon}"
        super().__init__(self.message)

