# app/domain/exceptions/tipodoc.py

class TipoDocNoEncontrado(Exception):
    """Se lanza cuando no se encuentra un tipodoc con el ID proporcionado."""
    def __init__(self, tipodoc_id: int):
        self.tipodoc_id = tipodoc_id
        self.message = f"TipoDoc con ID {tipodoc_id} no encontrado"
        super().__init__(self.message)


class TipoDocDuplicado(Exception):
    """Se lanza cuando se intenta crear un tipodoc con un valor único duplicado (ej. email o CUIT)."""
    def __init__(self, campo: str, valor: str):
        self.campo = campo
        self.valor = valor
        self.message = f"Ya existe un tipodoc con {campo} = {valor}"
        super().__init__(self.message)


class TipoDocInvalido(Exception):
    """Se lanza cuando los datos del tipodoc no cumplen alguna regla de negocio del dominio."""
    def __init__(self, razon: str):
        self.message = f"TipoDoc inválido: {razon}"
        super().__init__(self.message)

