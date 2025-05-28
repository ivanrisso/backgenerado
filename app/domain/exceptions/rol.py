# app/domain/exceptions/rol.py

class RolNoEncontrado(Exception):
    """Se lanza cuando no se encuentra un rol con el ID proporcionado."""
    def __init__(self, rol_id: int):
        self.rol_id = rol_id
        self.message = f"Rol con ID {rol_id} no encontrado"
        super().__init__(self.message)


class RolDuplicado(Exception):
    """Se lanza cuando se intenta crear un rol con un valor único duplicado (ej. email o CUIT)."""
    def __init__(self, campo: str, valor: str):
        self.campo = campo
        self.valor = valor
        self.message = f"Ya existe un rol con {campo} = {valor}"
        super().__init__(self.message)


class RolInvalido(Exception):
    """Se lanza cuando los datos del rol no cumplen alguna regla de negocio del dominio."""
    def __init__(self, razon: str):
        self.message = f"Rol inválido: {razon}"
        super().__init__(self.message)

