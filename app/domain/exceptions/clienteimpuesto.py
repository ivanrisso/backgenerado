# app/domain/exceptions/clienteimpuesto.py

class ClienteImpuestoNoEncontrado(Exception):
    """Se lanza cuando no se encuentra un clienteimpuesto con el ID proporcionado."""
    def __init__(self, clienteimpuesto_id: int):
        self.clienteimpuesto_id = clienteimpuesto_id
        self.message = f"ClienteImpuesto con ID {clienteimpuesto_id} no encontrado"
        super().__init__(self.message)


class ClienteImpuestoDuplicado(Exception):
    """Se lanza cuando se intenta crear un clienteimpuesto con un valor único duplicado (ej. email o CUIT)."""
    def __init__(self, campo: str, valor: str):
        self.campo = campo
        self.valor = valor
        self.message = f"Ya existe un clienteimpuesto con {campo} = {valor}"
        super().__init__(self.message)


class ClienteImpuestoInvalido(Exception):
    """Se lanza cuando los datos del clienteimpuesto no cumplen alguna regla de negocio del dominio."""
    def __init__(self, razon: str):
        self.message = f"ClienteImpuesto inválido: {razon}"
        super().__init__(self.message)

