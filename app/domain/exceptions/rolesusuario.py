# app/domain/exceptions/rolesusuario.py

class RolesUsuarioNoEncontrado(Exception):
    """Se lanza cuando no se encuentra un rolesusuario con el ID proporcionado."""
    def __init__(self, rolesusuario_id: int):
        self.rolesusuario_id = rolesusuario_id
        self.message = f"RolesUsuario con ID {rolesusuario_id} no encontrado"
        super().__init__(self.message)


class RolesUsuarioDuplicado(Exception):
    """Se lanza cuando se intenta crear un rolesusuario con un valor único duplicado (ej. email o CUIT)."""
    def __init__(self, campo: str, valor: str):
        self.campo = campo
        self.valor = valor
        self.message = f"Ya existe un rolesusuario con {campo} = {valor}"
        super().__init__(self.message)


class RolesUsuarioInvalido(Exception):
    """Se lanza cuando los datos del rolesusuario no cumplen alguna regla de negocio del dominio."""
    def __init__(self, razon: str):
        self.message = f"RolesUsuario inválido: {razon}"
        super().__init__(self.message)

