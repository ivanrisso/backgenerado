# Frontend Routes Inventory

## Lazy Imports
All routes use lazy loading.

### Auth
- /login -> @modules/Auth/ui/views/LoginView.vue
- /usuarios -> @modules/Auth/ui/views/UsuarioList.vue
- /roles -> @modules/Auth/ui/views/RolList.vue
- /menus -> @modules/Auth/ui/views/MenuItemTree.vue

### Clientes
- /clientes -> @modules/Clientes/ui/views/ClienteList.vue
- /clientes/deudores -> @modules/Clientes/ui/views/ClienteDeudorList.vue
- /clientes/:clienteId/domicilios/:domicilioId/telefonos -> @modules/Clientes/ui/views/ClienteTelefonosView.vue
- /cuentacorriente -> @modules/Clientes/ui/views/CurrentAccountView.vue

### Maestros
- /monedas -> MonedaView
- /ivas -> IvaView
- /conceptos -> ConceptoView
- /tipos-comprobante -> TipoComprobanteView
- /tipos-impuesto -> TipoImpuestoView
- /paises -> PaisView
- /provincias -> ProvinciaView
- /localidades -> LocalidadView
- /tipodoms -> TipoDomView
- /tipotels -> TipoTelView
- /operadores -> OperadorView
- /domicilios -> DomicilioView
- /telefonos -> TelefonoView
- /tipodocs -> TipoDocView
- /condiciones-tributarias -> CondicionTributariaView
- /puntos-venta -> PuntoVentaList
- /config/afip -> AfipConfigView

### Facturacion
- /comprobantes/nuevo -> @modules/Facturacion/ui/views/InvoiceCreateView.vue
- /comprobantes -> @modules/Facturacion/ui/views/InvoiceListView.vue

### Tesoreria
- /recibos/nuevo -> @modules/Tesoreria/ui/views/ReciboCreateView.vue
**NOTE:** Missing List View for Recibos.

### Shared
- /403 -> ForbiddenView
