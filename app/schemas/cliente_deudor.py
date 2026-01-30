from app.schemas.cliente import ClienteResponse

class ClienteDeudorResponse(ClienteResponse):
    saldo: float
