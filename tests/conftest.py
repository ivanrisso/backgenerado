
import pytest_asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from unittest.mock import MagicMock

# --- Fixtures de FastAPI ---
@pytest_asyncio.fixture
async def async_client():
    """Cliente HTTP asíncrono para tests de integración."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

# --- Fixtures de Mocking AFIP (CRÍTICO) ---
@pytest.fixture(autouse=True)
def mock_afip_wsaa(mocker):
    """
    Mock automático para WSAAClient.
    Previene llamadas reales a autenticación y evita uso de afip_token_cache.json.
    """
    # Patch de la clase WsaaClient (TitleCase)
    mock_wsaa_class = mocker.patch("app.infrastructure.clients.wsaa_client.WsaaClient")
    
    # Instancia mock
    mock_instance = mock_wsaa_class.return_value
    
    # Método obtener_ticket (nombre real) devuelve tupla (token, sign)
    # NOTA: En wsaa_client.py el método es `obtener_ticket`, devuelve tuple.
    mock_instance.obtener_ticket.return_value = ("MOCK_TOKEN_WSAA_123456", "MOCK_SIGN_WSAA_ABCDEF")
    
    return mock_instance

@pytest.fixture(autouse=True)
def mock_afip_wsfe(mocker):
    """
    Mock automático para WSFEClient.
    Previene llamadas reales a facturación electrónica.
    """
    # Patch de la clase WsfeClient (TitleCase)
    mock_wsfe_class = mocker.patch("app.infrastructure.clients.wsfe_client.WsfeClient")
    
    # Instancia mock
    mock_instance = mock_wsfe_class.return_value
    
    # Mock de emitir_factura (nombre real, no emitir_comprobante)
    # wsfe_client.py: def emitir_factura(self, cae_request: Dict[str, Any]) -> Dict[str, Any]:
    # Devuelve dict con CAE, vtoCae, observaciones
    mock_instance.emitir_factura.return_value = {
        "CAE": "12345678901234",
        "vtoCae": "20991231",
        "observaciones": []
    }
    
    # Mock de consultar_estado (nombre real)
    mock_instance.consultar_estado.return_value = {
        "estado": "A",
        "CAE": "12345678901234",
        "nroCbte": 1,
        "puntoVenta": 1,
        "tipoCbte": 1,
        "fchProceso": "20240101"
    }

    return mock_instance
