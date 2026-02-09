# Backend Endpoint Inventory (Strict Mode)

Valid Sources:
- [x] Observed in Runtime
- [x] Frontend Reference (Code import/call)

## Observed
- `POST /api/v1/auth/token`
- `GET /api/v1/users/me`
- `GET /api/v1/usuarios/me/menu`
- `GET /api/v1/clientes`
- `GET /api/v1/recibos`
- `GET /api/v1/recibos/{id}`
- `GET /api/v1/comprobantes`

## Frontend Referenced
- `POST /api/v1/comprobantes`
- `POST /api/v1/recibos`
- `GET /api/v1/monedas`
- `GET /api/v1/condiciones-tributarias`
- `GET /api/v1/puntos-venta`
- `GET /api/v1/ivas`
- `GET /api/v1/tipos-comprobante`
- `GET /api/v1/tipos-impuesto`
- `GET /api/v1/conceptos`
- `GET /api/v1/tipodocs`
- `GET /api/v1/paises`
- `GET /api/v1/provincias`
- `GET /api/v1/localidades`
