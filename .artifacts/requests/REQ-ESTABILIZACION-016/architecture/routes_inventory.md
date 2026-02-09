# Route Inventory

## Dashboard
- `/` -> `@modules/Dashboard/ui/views/DashboardView.vue`

## Auth
- `/login` -> `@modules/Auth/ui/views/LoginView.vue`
- `/403` -> `@shared/ui/views/ForbiddenView.vue`
- `/usuarios` -> `@modules/Auth/ui/views/UsuarioList.vue`
- `/roles` -> `@modules/Auth/ui/views/RolList.vue`
- `/menus` -> `@modules/Auth/ui/views/MenuItemTree.vue`

## Clientes
- `/clientes` -> `@modules/Clientes/ui/views/ClienteList.vue`
- `/clientes/deudores` -> `@modules/Clientes/ui/views/ClienteDeudorList.vue`
- `/clientes/:clienteId/domicilios/:domicilioId/telefonos` -> `@modules/Clientes/ui/views/ClienteTelefonosView.vue`
- `/cuentacorriente` -> `@modules/Clientes/ui/views/CurrentAccountView.vue`

## Maestros (Reference Data)
- `/monedas`, `/ivas`, `/conceptos`, `/puntos-venta`
- `/tipos-comprobante`, `/tipos-impuesto`
- `/paises`, `/provincias`, `/localidades`
- `/tipodoms`, `/tipotels`, `/tipodocs`
- `/operadores`, `/domicilios` (Inactive), `/telefonos`
- `/condiciones-tributarias`
- `/config/afip`

## Facturacion
- `/comprobantes/nuevo` -> `@modules/Facturacion/ui/views/InvoiceCreateView.vue`
- `/comprobantes` -> `@modules/Facturacion/ui/views/InvoiceListView.vue`

## Tesoreria
- `/recibos` -> `@modules/Tesoreria/ui/views/ReciboListView.vue`
- `/recibos/nuevo` -> `@modules/Tesoreria/ui/views/ReciboCreateView.vue`
- `/recibos/:id` -> `@modules/Tesoreria/ui/views/ReciboDetailView.vue`
