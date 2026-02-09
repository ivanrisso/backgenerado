# Backend Endpoint Inventory

## Auth
- `POST /api/v1/auth/token` (Login)
- `GET /api/v1/users/me` (Profile/Roles)
- `GET /api/v1/usuarios/me/menu` (Dynamic Menu - New)

## Clientes
- `GET /api/v1/clientes`
- `GET /api/v1/clientes/{id}/domicilios`
- `GET /api/v1/cuentacorriente`

## Facturación
- `GET /api/v1/comprobantes`
- `POST /api/v1/comprobantes`

## Tesorería
- `GET /api/v1/recibos`
- `POST /api/v1/recibos`
- `GET /api/v1/recibos/{id}`
- `DELETE /api/v1/recibos/{id}`
- `PUT /api/v1/recibos/{id}`

## Maestros
- `GET /api/v1/monedas`
- `GET /api/v1/ivas`
- `GET /api/v1/conceptos`
- `GET /api/v1/puntos-venta`
