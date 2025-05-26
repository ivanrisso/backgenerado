# app/domain/exceptions/base.py

class ErrorDeRepositorio(Exception):
    """Error técnico inesperado al interactuar con la base de datos."""
    def __init__(self, message: str = "Error de infraestructura en repositorio"):
        super().__init__(message)


class BaseDeDatosNoDisponible(Exception):
    """Error por conexión fallida a la base de datos."""
    def __init__(self, message: str = "No se pudo conectar a la base de datos"):
        super().__init__(message)
