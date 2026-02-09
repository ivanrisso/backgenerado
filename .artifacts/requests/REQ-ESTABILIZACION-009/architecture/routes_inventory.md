# Route Inventory

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

## Maestros
- `/monedas` -> `@modules/Maestros/ui/views/MonedaView.vue`
- `/ivas` -> `@modules/Maestros/ui/views/IvaView.vue`
- `/conceptos` -> `@modules/Maestros/ui/views/ConceptoView.vue`
- `/tipos-comprobante` -> `@modules/Maestros/ui/views/TipoComprobanteView.vue`
- `/tipos-impuesto` -> `@modules/Maestros/ui/views/TipoImpuestoView.vue`
- `/paises` -> `@modules/Maestros/ui/views/PaisView.vue`
- `/provincias` -> `@modules/Maestros/ui/views/ProvinciaView.vue`
- `/localidades` -> `@modules/Maestros/ui/views/LocalidadView.vue`
- `/tipodoms` -> `@modules/Maestros/ui/views/TipoDomView.vue`
- `/tipotels` -> `@modules/Maestros/ui/views/TipoTelView.vue`
- `/operadores` -> `@modules/Maestros/ui/views/OperadorView.vue`
- `/domicilios` -> `@modules/Maestros/ui/views/DomicilioView.vue`
- `/telefonos` -> `@modules/Maestros/ui/views/TelefonoView.vue`
- `/tipodocs` -> `@modules/Maestros/ui/views/TipoDocView.vue`
- `/condiciones-tributarias` -> `@modules/Maestros/ui/views/CondicionTributariaView.vue`
- `/puntos-venta` -> `@modules/Maestros/ui/views/PuntoVentaList.vue`

## Config
- `/config/afip` -> `@modules/Maestros/ui/views/AfipConfigView.vue`

## Facturacion
- `/comprobantes/nuevo` -> `@modules/Facturacion/ui/views/InvoiceCreateView.vue`
- `/comprobantes` -> `@modules/Facturacion/ui/views/InvoiceListView.vue`

## Tesoreria
- `/recibos` -> `@modules/Tesoreria/ui/views/ReciboListView.vue`
- `/recibos/nuevo` -> `@modules/Tesoreria/ui/views/ReciboCreateView.vue`
- `/recibos/:id` -> `@modules/Tesoreria/ui/views/ReciboDetailView.vue`
- `/recibos/imprimir/:id` -> `@modules/Tesoreria/ui/views/ReciboPrintView.vue`
- `/recibos/eliminar/:id` -> `@modules/Tesoreria/ui/views/ReciboDeleteView.vue`
- `/recibos/modificar/:id` -> `@modules/Tesoreria/ui/views/ReciboModifyView.vue`
