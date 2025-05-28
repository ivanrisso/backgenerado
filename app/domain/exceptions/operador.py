# app/domain/exceptions/operador.py

class OperadorNoEncontrado(Exception):
    """Se lanza cuando no se encuentra un operador con el ID proporcionado."""
    def __init__(self, operador_id: int):
        self.operador_id = operador_id
        self.message = f"Operador con ID {operador_id} no encontrado"
        super().__init__(self.message)


class OperadorDuplicado(Exception):
    """Se lanza cuando se intenta crear un operador con un valor único duplicado (ej. email o CUIT)."""
    def __init__(self, campo: str, valor: str):
        self.campo = campo
        self.valor = valor
        self.message = f"Ya existe un operador con {campo} = {valor}"
        super().__init__(self.message)


class OperadorInvalido(Exception):
    """Se lanza cuando los datos del operador no cumplen alguna regla de negocio del dominio."""
    def __init__(self, razon: str):
        self.message = f"Operador inválido: {razon}"
        super().__init__(self.message)

