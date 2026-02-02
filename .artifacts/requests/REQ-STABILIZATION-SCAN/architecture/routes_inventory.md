# Inventario de Rutas y Vistas

## 1. Contexto
Análisis estático del archivo `src/router/index.ts`.

## 2. Inventario de Rutas

| Ruta | Nombre | Componente (Lazy) | Protegido | Permisos |
|------|--------|-------------------|-----------|----------|
| `/login` | `login` | `LoginView` | ❌ | - |
| `/403` | `forbidden` | `ForbiddenView` | ❌ | - |
| `/` | - | `MainLayout` | ✅ | - |
| `/usuarios` | `usuarios` | `UsuarioList` | ✅ | - |
| `/clientes` | `clientes` | `ClienteList` | ✅ | - |
| `/clientes/deudores` | `clientes-deudores` | `ClienteDeudorList` | ✅ | - |
| `/clientes/:id/dom...` | `cliente-dom...` | `ClienteTelefonosView`| ✅ | - |
| `/roles` | `roles` | `RolList` | ✅ | - |
| `/menus` | `menus` | `MenuItemTree` | ✅ | - |
| `/monedas` | `monedas` | `MonedaView` | ✅ | - |
| `/ivas` | `ivas` | `IvaView` | ✅ | - |
| `/conceptos` | `conceptos` | `ConceptoView` | ✅ | - |
| `/tipos-comprobante` | `tipos-comprobante` | `TipoComprobanteView` | ✅ | - |
| `/tipos-impuesto` | `tipos-impuesto` | `TipoImpuestoView` | ✅ | - |
| `/paises` | `paises` | `PaisView` | ✅ | - |
| `/provincias` | `provincias` | `ProvinciaView` | ✅ | - |
| `/localidades` | `localidades` | `LocalidadView` | ✅ | - |
| `/tipodoms` | `tipodoms` | `TipoDomView` | ✅ | - |
| `/tipotels` | `tipotels` | `TipoTelView` | ✅ | - |
| `/operadores` | `operadores` | `OperadorView` | ✅ | - |
| `/domicilios` | `domicilios` | `DomicilioView` | ✅ | - |
| `/telefonos` | `telefonos` | `TelefonoView` | ✅ | - |
| `/tipodocs` | `tipodocs` | `TipoDocView` | ✅ | - |
| `/condiciones-trib...`| `condiciones-trib...`| `CondicionTributariaView`| ✅ | - |
| `/comprobantes/nuevo` | `comprobante-nuevo` | `InvoiceCreateView` | ✅ | - |
| `/comprobantes` | `comprobantes` | `InvoiceListView` | ✅ | - |
| `/recibos/nuevo` | `recibo-nuevo` | `ReciboCreateView` | ✅ | - |
| `/cuentacorriente` | `cuentacorriente` | `CurrentAccountView` | ✅ | - |

## 3. Comentarios
- Integridad de rutas verificada.
