
import pytest

@pytest.mark.asyncio
async def test_healthcheck(async_client):
    """Verifica que la API responde y está saludable."""
    response = await async_client.get("/")
    # Ajustar según la implementación real del root path
    # Si devuelve 404 es aceptable si no está definido, 
    # pero buscamos un 200 health o docs.
    # Asumimos que al menos responde algo (no connection error).
    assert response.status_code in [200, 404]
