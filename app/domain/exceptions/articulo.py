class ArticuloNoEncontrado(Exception):
    def __init__(self, identifier: str):
        self.message = f"Articulo con identificador '{identifier}' no encontrado."
        super().__init__(self.message)

class ArticuloDuplicado(Exception):
    def __init__(self, field: str, value: str):
        self.message = f"Ya existe un Articulo con {field}='{value}'."
        super().__init__(self.message)

class ArticuloInvalido(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
