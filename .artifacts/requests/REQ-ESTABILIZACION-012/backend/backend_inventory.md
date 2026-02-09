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

## Frontend Referenced (To be validated in Runtime)
- `POST /api/v1/comprobantes` (Invoice Creation)
- `POST /api/v1/recibos` (Receipt Creation)
- `GET /api/v1/monedas`
- `GET /api/v1/condiciones-tributarias`
- `GET /api/v1/puntos-venta`
