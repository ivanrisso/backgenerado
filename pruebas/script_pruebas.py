# script_pruebas.py
# -*- coding: utf-8 -*-
"""
Generador automático de suite de tests pytest a partir del openapi.yaml.
Al ejecutarlo, creará o sobrescribirá tests/test_api_generated.py.
"""

import os
import yaml

# Ruta de entrada y salida
BASE_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(BASE_DIR)
SPEC_PATH = os.path.join(BASE_DIR, "openapi.yaml")
OUT_DIR = os.path.join(ROOT_DIR, "tests")
OUT_FILE = os.path.join(OUT_DIR, "test_api_generated.py")



# Lee el spec
with open(SPEC_PATH, "r", encoding="utf-8") as f:
    spec = yaml.safe_load(f)

# Cabecera fija del archivo de tests
TEMPLATE = '''\
# tests/test_api_generated.py
# -*- coding: utf-8 -*-
"""
Suite de pruebas generada automáticamente a partir de openapi.yaml.
Framework: pytest + httpx + pyyaml + Faker + pytest-asyncio.
Comentarios y nombres en español.
"""

import os
import yaml
import pytest
from httpx import AsyncClient
from faker import Faker

# -------------------------------
# Fixtures
# -------------------------------
@pytest.fixture(scope="session")
def faker_es():
    return Faker('es_AR')

@pytest.fixture
async def api_client():
    base = os.getenv("API_URL", "http://localhost:8000")
    async with AsyncClient(base_url=base, follow_redirects=True) as c:
        yield c

@pytest.fixture
async def auth_headers(api_client, faker_es):
    try:
        with open(os.path.join(os.path.dirname(__file__), "openapi.yaml"), 'r', encoding='utf-8') as f:
            spec = yaml.safe_load(f)
        reg_rb = spec['paths']['/auth/register']['post']['requestBody']
        content = reg_rb.get('content', {}).get('application/json', {})
        ref = content.get('schema', {}).get('$ref')
        schema = spec['components']['schemas'][ref.split('/')[-1]]
        payload = {}
        for campo in schema.get('required', []):
            if 'email' in campo:
                payload[campo] = faker_es.email()
            else:
                payload[campo] = faker_es.word()
        payload['password'] = 'Password123!'
        r1 = await api_client.post('/auth/register/', json=payload)
        assert r1.status_code == 201
        login = {'email': payload['email'], 'password': payload['password']}
        r2 = await api_client.post('/auth/login/', json=login)
        token = r2.json().get('access_token')
        return {'Authorization': f'Bearer {token}'} if token else {}
    except Exception:
        return {}
'''

# Procesamiento de seguridad global
SEC_GLOBAL = spec.get("security", [])

def ruta_requiere_auth(path_item: dict) -> bool:
    return bool(path_item.get("security", SEC_GLOBAL))

def construir_payload_minimo(request_body: dict) -> dict:
    content = request_body.get('content', {}).get('application/json', {})
    ref = content.get('schema', {}).get('$ref')
    if not ref:
        return {}
    schema = spec['components']['schemas'][ref.split('/')[-1]]
    payload = {}
    for campo in schema.get('required', []):
        tipo = schema['properties'][campo].get('type', 'string')
        if tipo == 'integer':
            payload[campo] = 1
        elif tipo == 'number':
            payload[campo] = 1.0
        elif tipo == 'boolean':
            payload[campo] = True
        else:
            payload[campo] = f"test_{campo}"
    return payload

# Construcción dinámica de recursos
recursos_code = []
for path, methods in spec['paths'].items():
    ruta = path if path.endswith('/') else path + '/'
    for mtd, deta in methods.items():
        m = mtd.upper()
        if m not in ['GET', 'POST', 'PATCH', 'DELETE']:
            continue
        protegido = ruta_requiere_auth(deta)
        payload = {}
        if m in ['POST', 'PATCH'] and 'requestBody' in deta:
            payload = construir_payload_minimo(deta['requestBody'])
        recursos_code.append(f'    {{"ruta": "{ruta}", "metodo": "{m}", "payload": {payload}, "protegido": {protegido}}},')

RECURSOS_BLOCK = "RECURSOS = [\n" + "\n".join(recursos_code) + "\n]\n"

# Tests parametrizados
TESTS_BLOCK = '''
# -------------------------------
# Tests parametrizados
# -------------------------------

@pytest.mark.asyncio
@pytest.mark.parametrize("rec", RECURSOS)
async def test_happy_path(api_client, faker_es, auth_headers, rec):
    ruta = rec["ruta"]
    metodo = rec["metodo"]
    payload = rec["payload"]
    protegido = rec["protegido"]

    headers = auth_headers if protegido else {}
    url = ruta.replace("{id}", "1") if "{id}" in ruta else ruta
    body = None
    if metodo in ['POST', 'PATCH']:
        for k in payload:
            if isinstance(payload[k], str):
                payload[k] = faker_es.word()
        body = payload

    resp = await api_client.request(metodo, url, json=body, headers=headers)

    if protegido:
        assert resp.status_code in (200, 201), f"{metodo} {ruta} protegido devolvió {resp.status_code}"
    else:
        assert resp.status_code in (200, 201, 422), f"{metodo} {ruta} público devolvió {resp.status_code}"

@pytest.mark.asyncio
@pytest.mark.parametrize("rec", [r for r in RECURSOS if r["metodo"] in ['POST','PATCH']])
async def test_error_validacion_422(api_client, auth_headers, rec):
    ruta, metodo, protegido = rec["ruta"], rec["metodo"], rec["protegido"]
    headers = auth_headers if protegido else {}
    resp = await api_client.request(metodo, ruta, json={}, headers=headers)
    assert resp.status_code == 422

@pytest.mark.asyncio
@pytest.mark.parametrize("rec", [r for r in RECURSOS if r["metodo"] in ['GET','DELETE']])
async def test_not_found_404(api_client, auth_headers, rec):
    ruta, metodo, protegido = rec["ruta"], rec["metodo"], rec["protegido"]
    if "{id}" not in ruta:
        pytest.skip("No aplica sin {id}")
    url = ruta.replace("{id}", "999999")
    headers = auth_headers if protegido else {}
    resp = await api_client.request(metodo, url, headers=headers)
    assert resp.status_code == 404
'''

# Asegura el directorio de salida
os.makedirs(OUT_DIR, exist_ok=True)

# Escribe el archivo final
with open(OUT_FILE, "w", encoding="utf-8") as out:
    out.write(TEMPLATE)
    out.write("\n")
    out.write(RECURSOS_BLOCK)
    out.write("\n")
    out.write(TESTS_BLOCK)

print(f"✅ Tests generados en: {OUT_FILE}")
