# ✅ app/domain/exceptions/afip.py

class ErrorAfip(Exception):
    """Error relacionado con la comunicación o validación con AFIP."""

    def __init__(self, mensaje: str = "Error en la respuesta de AFIP", codigo: str = None, causa: str = None):
        self.mensaje = mensaje
        self.codigo = codigo
        self.causa = causa
        super().__init__(self.__str__())

    def __str__(self):
        if self.codigo:
            return f"[AFIP:{self.codigo}] {self.mensaje} - {self.causa or 'Sin detalle'}"
        return self.mensaje
