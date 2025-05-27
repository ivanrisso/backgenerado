# app/domain/exceptions/Usuario.py
class UsuarioNoEncontrado(Exception):
    """Se lanza cuando no se encuentra un Usuario con el ID proporcionado."""
    def __init__(self, Usuario_id: int):
        self.Usuario_id = Usuario_id
        self.message = f"Usuario con ID {Usuario_id} no encontrado"
        super().__init__(self.message)


class UsuarioDuplicado(Exception):
    """Se lanza cuando se intenta crear un Usuario con un valor único duplicado (ej. email o CUIT)."""
    def __init__(self, campo: str, valor: str):
        self.campo = campo
        self.valor = valor
        self.message = f"Ya existe un Usuario con {campo} = {valor}"
        super().__init__(self.message)


class UsuarioInvalido(Exception):
    """Se lanza cuando los datos del Usuario no cumplen alguna regla de negocio del dominio."""
    def __init__(self, razon: str):
        self.message = f"Usuario inválido: {razon}"
        super().__init__(self.message)

