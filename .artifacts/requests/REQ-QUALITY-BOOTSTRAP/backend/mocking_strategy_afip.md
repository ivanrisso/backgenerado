# AFIP Mocking Strategy

## Objetivo
Aislar la lógica de negocio y los tests de integración de la disponibilidad y efectos colaterales de los servicios de AFIP (WSAA / WSFE).

## Puntos de Intercepción

### 1. `WSAAClient` (Autenticación)
- **Archivo**: `app/infrastructure/clients/wsaa_client.py`
- **Método a mockear**: `get_token_sign()` o `authenticate()`
- **Comportamiento Mock**:
  - Devolver un objeto `TokenSign` válido con fecha de expiración futura.
  - Evitar lectura/escritura de `afip_token_cache.json` en tests.

### 2. `WSFEClient` (Facturación)
- **Archivo**: `app/infrastructure/clients/wsfe_client.py`
- **Método a mockear**: `emitir_comprobante()`, `consultar_comprobante()`
- **Comportamiento Mock**:
  - `emitir_comprobante`:
    - **Caso OK**: Devolver estructura con `CAE="12345678901234"` y `Vencimiento="2099....."`.
    - **Caso Rechazo**: Devolver array de `Errors` simulando validación de negocio (ej. CUIT inválido).
    - **Caso Timeout**: Lanzar excepción `requests.exceptions.Timeout`.

## Herramientas
- **Pytest**: `pytest-mock` (`mocker` fixture).
- **Patch**: `with patch('app.infrastructure.clients.wsaa_client.WSAAClient.get_token_sign')`

## Ejemplo de Fixture (Pseudo-código)

```python
import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_afip(mocker):
    # Mock WSAA
    mock_wsaa = mocker.patch("app.infrastructure.clients.wsaa_client.WSAAClient.get_token_sign")
    mock_wsaa.return_value = {"token": "mock_token", "sign": "mock_sign", "expiration": "2099-01-01T00:00:00"}
    
    # Mock WSFE
    mock_wsfe = mocker.patch("app.infrastructure.clients.wsfe_client.WSFEClient.emitir_comprobante")
    mock_wsfe.return_value = {"CAE": "12345678901234", "CAEFchVto": "20300101"}
    
    return mock_wsfe
```

## Reglas
1. **NUNCA** configurar credenciales reales de producción en entornos de test.
2. Los tests de CI deben fallar si intentan conectar a internet (usar plugin `pytest-socket` idealmente).
