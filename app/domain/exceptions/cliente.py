# app/domain/exceptions/cliente.py

class ClienteNoEncontrado(Exception):
    """Se lanza cuando no se encuentra un cliente con el ID proporcionado."""
    def __init__(self, cliente_id: int):
        self.cliente_id = cliente_id
        self.message = f"Cliente con ID {cliente_id} no encontrado"
        super().__init__(self.message)


class ClienteDuplicado(Exception):
    """Se lanza cuando se intenta crear un cliente con un valor único duplicado (ej. email o CUIT)."""
    def __init__(self, campo: str, valor: str):
        self.campo = campo
        self.valor = valor
        self.message = f"Ya existe un cliente con {campo} = {valor}"
        super().__init__(self.message)


class ClienteInvalido(Exception):
    """Se lanza cuando los datos del cliente no cumplen alguna regla de negocio del dominio."""
    def __init__(self, razon: str):
        self.message = f"Cliente inválido: {razon}"
        super().__init__(self.message)

