# ✅ app/domain/exceptions/afip.py
from fastapi import HTTPException

class ErrorAfip(HTTPException):
    """Error relacionado con la comunicación o validación con AFIP."""

    def __init__(self, mensaje: str = "Error en la respuesta de AFIP", codigo: str = None, causa: str = None):
        detail = f"[AFIP:{codigo}] {mensaje} - {causa or 'Sin detalle'}" if codigo else f"{mensaje} - {causa or 'Sin detalle'}"
        super().__init__(status_code=502, detail=detail)