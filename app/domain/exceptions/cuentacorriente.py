# app/domain/exceptions/cuentacorriente.py

class CuentaCorrienteNoEncontrado(Exception):
    """Se lanza cuando no se encuentra un cuentacorriente con el ID proporcionado."""
    def __init__(self, cuentacorriente_id: int):
        self.cuentacorriente_id = cuentacorriente_id
        self.message = f"CuentaCorriente con ID {cuentacorriente_id} no encontrado"
        super().__init__(self.message)


class CuentaCorrienteDuplicado(Exception):
    """Se lanza cuando se intenta crear un cuentacorriente con un valor único duplicado (ej. email o CUIT)."""
    def __init__(self, campo: str, valor: str):
        self.campo = campo
        self.valor = valor
        self.message = f"Ya existe un cuentacorriente con {campo} = {valor}"
        super().__init__(self.message)


class CuentaCorrienteInvalido(Exception):
    """Se lanza cuando los datos del cuentacorriente no cumplen alguna regla de negocio del dominio."""
    def __init__(self, razon: str):
        self.message = f"CuentaCorriente inválido: {razon}"
        super().__init__(self.message)

