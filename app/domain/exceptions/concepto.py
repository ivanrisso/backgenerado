# app/domain/exceptions/concepto.py

class ConceptoNoEncontrado(Exception):
    """Se lanza cuando no se encuentra un concepto con el ID proporcionado."""
    def __init__(self, concepto_id: int):
        self.concepto_id = concepto_id
        self.message = f"Concepto con ID {concepto_id} no encontrado"
        super().__init__(self.message)


class ConceptoDuplicado(Exception):
    """Se lanza cuando se intenta crear un concepto con un valor único duplicado (ej. email o CUIT)."""
    def __init__(self, campo: str, valor: str):
        self.campo = campo
        self.valor = valor
        self.message = f"Ya existe un concepto con {campo} = {valor}"
        super().__init__(self.message)


class ConceptoInvalido(Exception):
    """Se lanza cuando los datos del concepto no cumplen alguna regla de negocio del dominio."""
    def __init__(self, razon: str):
        self.message = f"Concepto inválido: {razon}"
        super().__init__(self.message)

