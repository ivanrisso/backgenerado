# app/domain/exceptions/rolmenuitem.py

class RolMenuItemNoEncontrado(Exception):
    """Se lanza cuando no se encuentra un rolmenuitem con el ID proporcionado."""
    def __init__(self, rolmenuitem_id: int):
        self.rolmenuitem_id = rolmenuitem_id
        self.message = f"RolMenuItem con ID {rolmenuitem_id} no encontrado"
        super().__init__(self.message)


class RolMenuItemDuplicado(Exception):
    """Se lanza cuando se intenta crear un rolmenuitem con un valor único duplicado (ej. email o CUIT)."""
    def __init__(self, campo: str, valor: str):
        self.campo = campo
        self.valor = valor
        self.message = f"Ya existe un rolmenuitem con {campo} = {valor}"
        super().__init__(self.message)


class RolMenuItemInvalido(Exception):
    """Se lanza cuando los datos del rolmenuitem no cumplen alguna regla de negocio del dominio."""
    def __init__(self, razon: str):
        self.message = f"RolMenuItem inválido: {razon}"
        super().__init__(self.message)

