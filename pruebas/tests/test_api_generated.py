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

RECURSOS = [
    {"ruta": "/auth/register/", "metodo": "POST", "payload": {'usuario_email': 'test_usuario_email', 'usuario_password': 'test_usuario_password', 'nombre': 'test_nombre', 'apellido': 'test_apellido'}, "protegido": False},
    {"ruta": "/auth/login/", "metodo": "POST", "payload": {'usuario_email': 'test_usuario_email', 'usuario_password': 'test_usuario_password'}, "protegido": False},
    {"ruta": "/auth/refresh/", "metodo": "POST", "payload": {}, "protegido": False},
    {"ruta": "/auth/logout/", "metodo": "POST", "payload": {}, "protegido": False},
    {"ruta": "/auth/me/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/auditoriacomprobantes/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/auditoriacomprobantes/", "metodo": "POST", "payload": {'comprobante_id': 1, 'usuario_id': 1, 'accion': 'test_accion', 'detalle': 'test_detalle', 'ip_origen': 'test_ip_origen', 'fecha': 'test_fecha'}, "protegido": False},
    {"ruta": "/auditoriacomprobantes/{id}/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/clientes/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/clientes/", "metodo": "POST", "payload": {'nombre': 'test_nombre', 'apellido': 'test_apellido', 'email': 'test_email', 'tipo_doc_id': 1, 'iva_id': 1}, "protegido": False},
    {"ruta": "/clientes/{id}/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/clientes/{id}/", "metodo": "PATCH", "payload": {}, "protegido": False},
    {"ruta": "/clientes/{id}/", "metodo": "DELETE", "payload": {}, "protegido": False},
    {"ruta": "/clienteimpuestos/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/clienteimpuestos/", "metodo": "POST", "payload": {'cliente_id': 'test_cliente_id', 'tipo_impuesto_id': 'test_tipo_impuesto_id'}, "protegido": False},
    {"ruta": "/clienteimpuestos/{id}/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/comprobantes/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/comprobantes/", "metodo": "POST", "payload": {'cliente_id': 1, 'tipo_comprobante_id': 1, 'concepto_id': 1, 'tipo_doc_id': 1, 'moneda_id': 1, 'punto_venta': 1, 'numero': 1, 'fecha_emision': 'test_fecha_emision', 'doc_nro': 'test_doc_nro', 'nombre_cliente': 'test_nombre_cliente', 'cuit_cliente': 'test_cuit_cliente', 'domicilio_cliente': 'test_domicilio_cliente', 'localidad_cliente': 'test_localidad_cliente', 'cod_postal_cliente': 'test_cod_postal_cliente', 'provincia_cliente': 'test_provincia_cliente', 'cotizacion_moneda': 1.0, 'total_neto': 1.0, 'total_iva': 1.0, 'total_impuestos': 1.0, 'total': 1.0, 'observaciones': 'test_observaciones'}, "protegido": False},
    {"ruta": "/comprobantes/{id}/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/comprobantedetalles/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/comprobantedetalles/", "metodo": "POST", "payload": {'comprobante_id': 1, 'iva_id': 1, 'descripcion': 'test_descripcion', 'cantidad': 1.0, 'precio_unitario': 1.0, 'importe': 1.0, 'alicuota_iva': 1.0, 'importe_iva': 1.0}, "protegido": False},
    {"ruta": "/comprobantedetalles/{id}/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/comprobanteimpuestos/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/comprobanteimpuestos/", "metodo": "POST", "payload": {'comprobante_id': 1, 'tipo_impuesto_id': 1, 'descripcion': 'test_descripcion', 'base_imponible': 1.0, 'alicuota': 1.0, 'importe': 1.0}, "protegido": False},
    {"ruta": "/comprobanteimpuestos/{id}/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/conceptos/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/conceptos/", "metodo": "POST", "payload": {'codigo': 'test_codigo', 'descripcion': 'test_descripcion'}, "protegido": False},
    {"ruta": "/conceptos/{id}/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/cuentacorrientes/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/cuentacorrientes/", "metodo": "POST", "payload": {'cliente_id': 1, 'comprobante_id': 'test_comprobante_id', 'fecha': 'test_fecha', 'tipo': 'test_tipo', 'importe': 1.0, 'signo': 1}, "protegido": False},
    {"ruta": "/cuentacorrientes/{id}/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/domicilios/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/domicilios/", "metodo": "POST", "payload": {'calle': 'test_calle', 'numero': 1, 'cliente_id': 1, 'tipo_dom_id': 1, 'localidad_id': 1}, "protegido": False},
    {"ruta": "/domicilios/{id}/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/ivas/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/ivas/", "metodo": "POST", "payload": {'codigo': 1, 'descripcion': 'test_descripcion', 'porcentaje': 'test_porcentaje', 'discriminado': True, 'porcentaje_sobre': 'test_porcentaje_sobre'}, "protegido": False},
    {"ruta": "/ivas/{id}/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/ivas/{id}/", "metodo": "PATCH", "payload": {}, "protegido": False},
    {"ruta": "/ivas/{id}/", "metodo": "DELETE", "payload": {}, "protegido": False},
    {"ruta": "/localidads/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/localidads/", "metodo": "POST", "payload": {'localidad_nombre': 'test_localidad_nombre', 'cod_postal': 'test_cod_postal', 'provincia_id': 'test_provincia_id'}, "protegido": False},
    {"ruta": "/localidads/{id}/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/menuitems/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/menuitems/", "metodo": "POST", "payload": {'nombre': 'test_nombre', 'path': 'test_path', 'parent_id': 'test_parent_id'}, "protegido": False},
    {"ruta": "/menuitems/{id}/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/monedas/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/monedas/", "metodo": "POST", "payload": {'codigo': 'test_codigo', 'descripcion': 'test_descripcion'}, "protegido": False},
    {"ruta": "/monedas/{id}/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/operadors/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/operadors/", "metodo": "POST", "payload": {'cliente_id': 'test_cliente_id'}, "protegido": False},
    {"ruta": "/operadors/{id}/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/paiss/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/paiss/", "metodo": "POST", "payload": {'codigo': 'test_codigo', 'nombre': 'test_nombre'}, "protegido": False},
    {"ruta": "/paiss/{id}/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/provincias/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/provincias/", "metodo": "POST", "payload": {'provincia_nombre': 'test_provincia_nombre', 'pais_id': 'test_pais_id'}, "protegido": False},
    {"ruta": "/provincias/{id}/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/rols/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/rols/", "metodo": "POST", "payload": {'rol_nombre': 'test_rol_nombre', 'es_admin': True}, "protegido": False},
    {"ruta": "/rols/{id}/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/rolesusuarios/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/rolesusuarios/", "metodo": "POST", "payload": {'usuario_id': 'test_usuario_id', 'rol_id': 'test_rol_id'}, "protegido": False},
    {"ruta": "/rolesusuarios/{id}/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/rolmenuitems/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/rolmenuitems/", "metodo": "POST", "payload": {'rol_id': 'test_rol_id', 'menu_item_id': 'test_menu_item_id'}, "protegido": False},
    {"ruta": "/rolmenuitems/{id}/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/telefonos/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/telefonos/", "metodo": "POST", "payload": {'tipo_tel_id': 1, 'prefijo': 'test_prefijo', 'numero': 'test_numero', 'domicilio_id': 1}, "protegido": False},
    {"ruta": "/telefonos/{id}/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/tipocomprobantes/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/tipocomprobantes/", "metodo": "POST", "payload": {'codigo': 'test_codigo', 'descripcion': 'test_descripcion', 'es_fiscal': 'test_es_fiscal'}, "protegido": False},
    {"ruta": "/tipocomprobantes/{id}/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/tipodocs/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/tipodocs/", "metodo": "POST", "payload": {'tipo_doc_nombre': 'test_tipo_doc_nombre', 'habilitado': True}, "protegido": False},
    {"ruta": "/tipodocs/{id}/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/tipodocs/{id}/", "metodo": "PATCH", "payload": {}, "protegido": False},
    {"ruta": "/tipodocs/{id}/", "metodo": "DELETE", "payload": {}, "protegido": False},
    {"ruta": "/tipodoms/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/tipodoms/", "metodo": "POST", "payload": {'nombre': 'test_nombre'}, "protegido": False},
    {"ruta": "/tipodoms/{id}/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/tipoimpuestos/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/tipoimpuestos/", "metodo": "POST", "payload": {'codigo_afip': 'test_codigo_afip', 'nombre': 'test_nombre', 'descripcion': 'test_descripcion', 'tipo_aplicacion': 'test_tipo_aplicacion', 'base_calculo': 'test_base_calculo', 'porcentaje': 'test_porcentaje', 'editable': True, 'obligatorio': True, 'activo': True}, "protegido": False},
    {"ruta": "/tipoimpuestos/{id}/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/tipotels/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/tipotels/", "metodo": "POST", "payload": {'nombre': 'test_nombre'}, "protegido": False},
    {"ruta": "/tipotels/{id}/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/usuarios/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/usuarios/", "metodo": "POST", "payload": {'usuario_email': 'test_usuario_email', 'usuario_password': 'test_usuario_password'}, "protegido": False},
    {"ruta": "/usuarios/{id}/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/usuarios/{id}/", "metodo": "PATCH", "payload": {}, "protegido": False},
    {"ruta": "/usuarios/{id}/", "metodo": "DELETE", "payload": {}, "protegido": False},
    {"ruta": "/usuarios/{usuario_mail}/", "metodo": "GET", "payload": {}, "protegido": False},
    {"ruta": "/ping/", "metodo": "GET", "payload": {}, "protegido": False},
]


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
