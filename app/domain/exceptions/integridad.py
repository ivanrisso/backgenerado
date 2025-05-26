class ClaveForaneaInvalida(Exception):
    def __init__(self, campo: str, valor: str = ""):
        self.campo = campo
        self.valor = valor
        mensaje = f"El valor '{valor}' para el campo '{campo}' no existe en la tabla referenciada"
        super().__init__(mensaje)
