# Backend API Inventory

## Resumen
- **Total Entities**: 32
- **Total Endpoints**: ~150
- **Authentication**: JWT Bearer (Global), Except Public Endpoints.

## Inventory by Entity

### Articulo
- `GET /api/v1/articulos/` (401)
- `POST /api/v1/articulos/`
- `GET /api/v1/articulos/{id}`
- `PATCH /api/v1/articulos/{id}`
- `DELETE /api/v1/articulos/{id}`

### AuditoriaComprobante
- `GET /api/v1/auditoriacomprobantes/` (401)
- `POST /api/v1/auditoriacomprobantes/`
- `GET /api/v1/auditoriacomprobantes/{id}`
- `PATCH /api/v1/auditoriacomprobantes/{id}`
- `DELETE /api/v1/auditoriacomprobantes/{id}`

### Autenticación (Auth)
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/logout`
- `GET /api/v1/auth/me` (401)
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/register`

### Cliente
- `GET /api/v1/clientes/` (401)
- `POST /api/v1/clientes/`
- `GET /api/v1/clientes/deudores` (401)
- `GET /api/v1/clientes/{id}`
- `PATCH /api/v1/clientes/{id}`
- `DELETE /api/v1/clientes/{id}`
- `GET /api/v1/clientes/{id}/sync-afip-taxes`
- `POST /api/v1/clientes/{id}/sync-afip-taxes`

### Comprobante
- `GET /api/v1/comprobantes/` (401)
- `POST /api/v1/comprobantes/`
- `POST /api/v1/comprobantes/from-voucher`
- `POST /api/v1/comprobantes/full/`
- `GET /api/v1/comprobantes/{id}`
- `PATCH /api/v1/comprobantes/{id}`
- `DELETE /api/v1/comprobantes/{id}`

### ComprobanteDetalle
- `GET /api/v1/comprobantedetalles/` (401)
- `POST /api/v1/comprobantedetalles/`
- `GET /api/v1/comprobantedetalles/{id}`
- `PATCH /api/v1/comprobantedetalles/{id}`
- `DELETE /api/v1/comprobantedetalles/{id}`

### ComprobanteImpuesto
- `GET /api/v1/comprobanteimpuestos/` (401)
- `POST /api/v1/comprobanteimpuestos/`
- `GET /api/v1/comprobanteimpuestos/{id}`
- `PATCH /api/v1/comprobanteimpuestos/{id}`
- `DELETE /api/v1/comprobanteimpuestos/{id}`

### Concepto
- `GET /api/v1/conceptos/` (401)
- `POST /api/v1/conceptos/`
- `GET /api/v1/conceptos/{id}`
- `PATCH /api/v1/conceptos/{id}`
- `DELETE /api/v1/conceptos/{id}`

### Condiciones Tributarias
- `GET /api/v1/condiciones-tributarias/` (200 OK - Public/Verified)
- `POST /api/v1/condiciones-tributarias/`
- `GET /api/v1/condiciones-tributarias/{id}`
- `PATCH /api/v1/condiciones-tributarias/{id}`
- `DELETE /api/v1/condiciones-tributarias/{id}`

### CuentaCorriente
- `GET /api/v1/cuentacorrientes/` (401)
- `POST /api/v1/cuentacorrientes/`
- `GET /api/v1/cuentacorrientes/{id}`
- `PATCH /api/v1/cuentacorrientes/{id}`
- `DELETE /api/v1/cuentacorrientes/{id}`

### Domicilio
- `GET /api/v1/domicilios/` (401)
- `POST /api/v1/domicilios/`
- `GET /api/v1/domicilios/{id}`
- `PATCH /api/v1/domicilios/{id}`
- `DELETE /api/v1/domicilios/{id}`

### Iva
- `GET /api/v1/ivas/` (401)
- `POST /api/v1/ivas/`
- `GET /api/v1/ivas/{id}`
- `PATCH /api/v1/ivas/{id}`
- `DELETE /api/v1/ivas/{id}`

### Localidad
- `GET /api/v1/localidades/` (401)
- `POST /api/v1/localidades/`
- `GET /api/v1/localidades/{id}`
- `PATCH /api/v1/localidades/{id}`
- `DELETE /api/v1/localidades/{id}`

### MenuItem
- `GET /api/v1/menuitems/` (401)
- `POST /api/v1/menuitems/`
- `GET /api/v1/menuitems/{id}`
- `PATCH /api/v1/menuitems/{id}`
- `DELETE /api/v1/menuitems/{id}`

### Moneda
- `GET /api/v1/monedas/` (401)
- `POST /api/v1/monedas/`
- `GET /api/v1/monedas/{id}`
- `PATCH /api/v1/monedas/{id}`
- `DELETE /api/v1/monedas/{id}`

### Operador
- `GET /api/v1/operadors/` (401)
- `POST /api/v1/operadors/`
- `GET /api/v1/operadors/{id}`
- `PATCH /api/v1/operadors/{id}`
- `DELETE /api/v1/operadors/{id}`

### Pais
- `GET /api/v1/paises/` (401)
- `POST /api/v1/paises/`
- `GET /api/v1/paises/{id}`
- `PATCH /api/v1/paises/{id}`
- `DELETE /api/v1/paises/{id}`

### Provincia
- `GET /api/v1/provincias/` (401)
- `POST /api/v1/provincias/`
- `GET /api/v1/provincias/{id}`
- `PATCH /api/v1/provincias/{id}`
- `DELETE /api/v1/provincias/{id}`

### Recibos
- `POST /api/v1/recibos/`

### RolesUsuario
- `GET /api/v1/rolesusuarios/` (401)
- `POST /api/v1/rolesusuarios/`
- `GET /api/v1/rolesusuarios/{id}`
- `PATCH /api/v1/rolesusuarios/{id}`
- `DELETE /api/v1/rolesusuarios/{id}`

### RolMenuItem
- `GET /api/v1/rolmenuitems/` (401)
- `POST /api/v1/rolmenuitems/`
- `GET /api/v1/rolmenuitems/{id}`
- `PATCH /api/v1/rolmenuitems/{id}`
- `DELETE /api/v1/rolmenuitems/{id}`

### Rol
- `GET /api/v1/rols/` (401)
- `POST /api/v1/rols/`
- `GET /api/v1/rols/{id}`
- `PATCH /api/v1/rols/{id}`
- `DELETE /api/v1/rols/{id}`

### Telefono
- `GET /api/v1/telefonos/` (401)
- `POST /api/v1/telefonos/`
- `GET /api/v1/telefonos/domicilio/{domicilio_id}`
- `GET /api/v1/telefonos/{id}`
- `PATCH /api/v1/telefonos/{id}`
- `DELETE /api/v1/telefonos/{id}`

### TipoComprobante
- `GET /api/v1/tipocomprobantes/` (401)
- `POST /api/v1/tipocomprobantes/`
- `GET /api/v1/tipocomprobantes/{id}`
- `PATCH /api/v1/tipocomprobantes/{id}`
- `DELETE /api/v1/tipocomprobantes/{id}`

### TipoDoc
- `GET /api/v1/tipodocs/` (401)
- `POST /api/v1/tipodocs/`
- `GET /api/v1/tipodocs/{id}`
- `PATCH /api/v1/tipodocs/{id}`
- `DELETE /api/v1/tipodocs/{id}`

### TipoDom
- `GET /api/v1/tipodoms/` (401)
- `POST /api/v1/tipodoms/`
- `GET /api/v1/tipodoms/{id}`
- `PATCH /api/v1/tipodoms/{id}`
- `DELETE /api/v1/tipodoms/{id}`

### TipoImpuesto
- `GET /api/v1/tipoimpuestos/` (401)
- `POST /api/v1/tipoimpuestos/`
- `GET /api/v1/tipoimpuestos/{id}`
- `PATCH /api/v1/tipoimpuestos/{id}`
- `DELETE /api/v1/tipoimpuestos/{id}`

### TipoTel
- `GET /api/v1/tipotels/` (401)
- `POST /api/v1/tipotels/`
- `GET /api/v1/tipotels/{id}`
- `PATCH /api/v1/tipotels/{id}`
- `DELETE /api/v1/tipotels/{id}`

### Usuario
- `GET /api/v1/usuarios/` (200 OK - Public?!)
- `POST /api/v1/usuarios/`
- `GET /api/v1/usuarios/{id}`
- `PATCH /api/v1/usuarios/{id}`
- `DELETE /api/v1/usuarios/{id}`
- `GET /api/v1/usuarios/{usuario_mail}`
