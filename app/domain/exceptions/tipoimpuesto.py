# app/domain/exceptions/tipoimpuesto.py

class TipoImpuestoNoEncontrado(Exception):
    """Se lanza cuando no se encuentra un tipoimpuesto con el ID proporcionado."""
    def __init__(self, tipoimpuesto_id: int):
        self.tipoimpuesto_id = tipoimpuesto_id
        self.message = f"TipoImpuesto con ID {tipoimpuesto_id} no encontrado"
        super().__init__(self.message)


class TipoImpuestoDuplicado(Exception):
    """Se lanza cuando se intenta crear un tipoimpuesto con un valor único duplicado (ej. email o CUIT)."""
    def __init__(self, campo: str, valor: str):
        self.campo = campo
        self.valor = valor
        self.message = f"Ya existe un tipoimpuesto con {campo} = {valor}"
        super().__init__(self.message)


class TipoImpuestoInvalido(Exception):
    """Se lanza cuando los datos del tipoimpuesto no cumplen alguna regla de negocio del dominio."""
    def __init__(self, razon: str):
        self.message = f"TipoImpuesto inválido: {razon}"
        super().__init__(self.message)

