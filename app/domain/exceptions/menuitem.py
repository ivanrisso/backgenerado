# app/domain/exceptions/menuitem.py

class MenuItemNoEncontrado(Exception):
    """Se lanza cuando no se encuentra un menuitem con el ID proporcionado."""
    def __init__(self, menuitem_id: int):
        self.menuitem_id = menuitem_id
        self.message = f"MenuItem con ID {menuitem_id} no encontrado"
        super().__init__(self.message)


class MenuItemDuplicado(Exception):
    """Se lanza cuando se intenta crear un menuitem con un valor único duplicado (ej. email o CUIT)."""
    def __init__(self, campo: str, valor: str):
        self.campo = campo
        self.valor = valor
        self.message = f"Ya existe un menuitem con {campo} = {valor}"
        super().__init__(self.message)


class MenuItemInvalido(Exception):
    """Se lanza cuando los datos del menuitem no cumplen alguna regla de negocio del dominio."""
    def __init__(self, razon: str):
        self.message = f"MenuItem inválido: {razon}"
        super().__init__(self.message)

