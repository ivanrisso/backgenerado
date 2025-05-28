# app/domain/exceptions/telefono.py

class TelefonoNoEncontrado(Exception):
    """Se lanza cuando no se encuentra un telefono con el ID proporcionado."""
    def __init__(self, telefono_id: int):
        self.telefono_id = telefono_id
        self.message = f"Telefono con ID {telefono_id} no encontrado"
        super().__init__(self.message)


class TelefonoDuplicado(Exception):
    """Se lanza cuando se intenta crear un telefono con un valor único duplicado (ej. email o CUIT)."""
    def __init__(self, campo: str, valor: str):
        self.campo = campo
        self.valor = valor
        self.message = f"Ya existe un telefono con {campo} = {valor}"
        super().__init__(self.message)


class TelefonoInvalido(Exception):
    """Se lanza cuando los datos del telefono no cumplen alguna regla de negocio del dominio."""
    def __init__(self, razon: str):
        self.message = f"Telefono inválido: {razon}"
        super().__init__(self.message)

