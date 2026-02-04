# Inventario de Rutas

**Total Rutas:** 26 (aprox)

## Auth
- `/login` -> `@modules/Auth/ui/views/LoginView.vue`
- `/403` -> `@shared/ui/views/ForbiddenView.vue`

## Usuarios y Roles
- `/usuarios` -> `@modules/Auth/ui/views/UsuarioList.vue` (Auth)
- `/roles` -> `@modules/Auth/ui/views/RolList.vue` (Auth)
- `/menus` -> `@modules/Auth/ui/views/MenuItemTree.vue` (Auth)

## Clientes
- `/clientes` -> `@modules/Clientes/ui/views/ClienteList.vue`
- `/clientes/deudores` -> `@modules/Clientes/ui/views/ClienteDeudorList.vue`
- `/clientes/:clienteId/domicilios/:domicilioId/telefonos` -> `@modules/Clientes/ui/views/ClienteTelefonosView.vue`
- `/cuentacorriente` -> `@modules/Clientes/ui/views/CurrentAccountView.vue`

## Facturación
- `/comprobantes` -> `@modules/Facturacion/ui/views/InvoiceListView.vue`
- `/comprobantes/nuevo` -> `@modules/Facturacion/ui/views/InvoiceCreateView.vue`

## Tesorería
- `/recibos/nuevo` -> `@modules/Tesoreria/ui/views/ReciboCreateView.vue`

## Maestros (Config)
- `/monedas` -> `@modules/Maestros/ui/views/MonedaView.vue`
- `/ivas` -> `@modules/Maestros/ui/views/IvaView.vue`
- `/conceptos` -> `@modules/Maestros/ui/views/ConceptoView.vue`
- `/tipos-comprobante` -> `@modules/Maestros/ui/views/TipoComprobanteView.vue`
- ... (Otros maestros)
- `/config/afip` -> `@modules/Maestros/ui/views/AfipConfigView.vue`
